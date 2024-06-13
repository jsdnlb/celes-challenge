from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, avg
from api.models.user import UserSchema
from security.authentication import verify_token

router = APIRouter()


def read_data(data_path):
    """
    Read data from parquet files.
    """
    spark = SparkSession.builder.appName("Read Parquet Files").getOrCreate()
    df = spark.read.parquet(data_path)
    return df


def get_sales_by_time_period(df, start_date: date, end_date: date, query_key: str):
    """
    Get sales data by time period for a specific query key.
    I will now explain some of the cases covered by FastAPI properties
    As for the dates, it validates if you enter a value less than 4 digits in the year,
    if the month value is greater than 12, if the day value is greater than 32 it will
    raise an EntityError.
    """
    if start_date > end_date:
        raise HTTPException(
            status_code=400, detail="Start date must be greater than end date"
        )

    if query_key not in ["KeyEmployee", "KeyProduct", "KeyStore"]:
        raise HTTPException(status_code=400, detail="Enter a valid query key")

    try:
        filtered_df = df.filter(
            (col("KeyDate") >= start_date) & (col("KeyDate") <= end_date)
        )

        # Grouping by query key and calculating total sales and total quantity sold
        sales_result = filtered_df.groupBy(query_key).agg(
            sum("Amount").alias("TotalSalesAmount"),
            sum("Qty").alias("TotalQuantitySold"),
        )

        # Convert the result to JSON using nested dictionaries
        result_json = [
            {
                query_key: row[query_key],
                "TotalSalesAmount": row["TotalSalesAmount"],
                "TotalQuantitySold": row["TotalQuantitySold"],
            }
            for row in sales_result.collect()
        ]

        return result_json

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_total_and_average_sales(df, query_key: str):
    """
    Get total and average sales data for a specific query key.
    """
    if query_key not in ["KeyEmployee", "KeyProduct", "KeyStore"]:
        raise HTTPException(status_code=400, detail="Enter a valid query key")

    try:
        sales_result = df.groupBy(query_key).agg(
            sum("Amount").alias("TotalAmount"),
            avg("Amount").alias("AvgAmount"),
        )

        # Convert the result to JSON
        result_json = [
            {
                query_key: row[query_key],
                "TotalAmount": row["TotalAmount"],
                "AvgAmount": row["AvgAmount"],
            }
            for row in sales_result.collect()
        ]

        return result_json

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sales_by_time_period/", tags=["Sales"])
def sales_by_time_period(
    start_date: date = "2023-01-01",
    end_date: date = "2023-12-01",
    query_key: str = "KeyStore",
    data_path: str = "data/",
    user: UserSchema = Depends(verify_token),
):
    """
    Get sales data by time period for a specific query key.
    """
    df = read_data(data_path)
    return get_sales_by_time_period(df, start_date, end_date, query_key)


@router.get("/total_and_average_sales/", tags=["Sales"])
def total_and_average_sales(
    query_key: str = "KeyStore",
    user: UserSchema = Depends(verify_token),
    data_path: str = "data/",
):
    """
    Get total and average sales data for a specific query key.
    """
    df = read_data(data_path)
    return get_total_and_average_sales(df, query_key)

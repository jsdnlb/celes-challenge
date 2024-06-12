from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, avg
from api.models.user import UserSchema
from security.authentication import verify_token


router = APIRouter()


# Create a Spark session
spark = SparkSession.builder.appName("Read Multiple Parquet Files").getOrCreate()

# Read all parquet files in the directory
df = spark.read.parquet("data/")


@router.get("/sales_by_time_period/", tags=["Sales"])
def sales_by_time_period(
    start_date: date,
    end_date: date,
    queryKey: str,
    user: UserSchema = Depends(verify_token),
):
    """
    I will now explain some of the cases covered by FastAPI properties
    As for the dates, it validates if you enter a value less than 4 digits in the year,
    if the month value is greater than 12, if the day value is greater than 32 it will
    raise an EntityError.
    """
    if start_date > end_date:
        raise HTTPException(
            status_code=400, detail="Start date must be greater than end date"
        )
    elif queryKey not in ["KeyEmployee", "KeyProduct", "KeyStore"]:
        raise HTTPException(status_code=400, detail="Enter a valid queryKey")

    try:
        filtered_df = df.filter(
            (col("KeyDate") >= start_date) & (col("KeyDate") <= end_date)
        )

        # Grouping by employee and calculating total sales and total quantity sold
        sales_result = filtered_df.groupBy(queryKey).agg(
            sum("Amount").alias("TotalSalesAmount"),
            sum("Qty").alias("TotalQuantitySold"),
        )

        # Convert the result to JSON using nested dictionaries
        result = sales_result.collect()
        result_json = [
            {
                queryKey: row[queryKey],
                "TotalSalesAmount": row["TotalSalesAmount"],
                "TotalQuantitySold": row["TotalQuantitySold"],
            }
            for row in result
        ]

        return result_json

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/total_and_average_sales/", tags=["Sales"])
def total_and_average_sales(
    queryKey: str,
    user: UserSchema = Depends(verify_token),
):
    if queryKey not in ["KeyEmployee", "KeyProduct", "KeyStore"]:
        raise HTTPException(status_code=400, detail="Enter a valid queryKey")

    try:
        sales_result = df.groupBy(queryKey).agg(
            sum("Amount").alias("TotalAmount"),
            avg("Amount").alias("AvgAmount"),
        )

        # Convert the result to JSON using nested dictionaries
        result = sales_result.collect()
        result_json = [
            {
                queryKey: row[queryKey],
                "TotalAmount": row["TotalAmount"],
                "AvgAmount": row["AvgAmount"],
            }
            for row in result
        ]

        return result_json

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

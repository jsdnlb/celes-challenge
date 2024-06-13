import os
import shutil
from pyspark.sql import SparkSession
from pyspark.sql.functions import to_date


def create_test_data(data_path):
    """
    Creates the necessary files for editing and testing
    """
    spark = SparkSession.builder.appName("Test Data").getOrCreate()
    data = [
        {
            "KeyDate": "2024-01-01",
            "KeyEmployee": 1,
            "KeyProduct": 101,
            "KeyStore": 1001,
            "Amount": 150.0,
            "Qty": 10,
        },
        {
            "KeyDate": "2024-01-02",
            "KeyEmployee": 1,
            "KeyProduct": 102,
            "KeyStore": 1001,
            "Amount": 200.0,
            "Qty": 20,
        },
        {
            "KeyDate": "2024-01-03",
            "KeyEmployee": 2,
            "KeyProduct": 101,
            "KeyStore": 1002,
            "Amount": 300.0,
            "Qty": 15,
        },
        {
            "KeyDate": "2024-01-04",
            "KeyEmployee": 3,
            "KeyProduct": 101,
            "KeyStore": 1002,
            "Amount": 1000.0,
            "Qty": 5,
        },
    ]
    df = spark.createDataFrame(data)
    df.write.parquet(data_path, mode="overwrite")
    return df


def setup_test_environment(data_path):
    """
    Creates the folder if it does not exist where the files will be stored
    """
    os.makedirs(data_path, exist_ok=True)
    create_test_data(data_path)


def teardown_test_environment(data_path):
    """
    Delete files after testing is completed
    """
    if os.path.exists(data_path):
        shutil.rmtree(data_path)


def sort_results(results, key):
    """
    Order the answers as sometimes some tests failed due to the order of the answers.
    """
    return sorted(results, key=lambda x: x[key])

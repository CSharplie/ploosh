import os
import pandas as pd
from pyspark.sql import SparkSession
import pytest
from pyjeb import control_and_setup
from ploosh.engines.load_engine_spark import LoadEngineSpark
from ploosh.configuration import Configuration
from ploosh.connectors.connector_parquet_spark import ConnectorParquetSpark

@pytest.fixture
def connector():
    spark = SparkSession.builder \
        .appName("ploosh") \
        .master("local[*]") \
        .config("spark.executor.memory", "1g") \
        .config("spark.driver.memory", "1g") \
        .getOrCreate()
    
    connector = ConnectorParquetSpark()
    connector.spark = spark

    return connector

@pytest.fixture
def df_sales():
    return pd.read_csv("./tests/.data/sales.csv", delimiter=",")

def test_default(connector, df_sales):
    configuration = {
       "path": "./tests/.env/parquet/sales.parquet",
    }

    configuration =  control_and_setup(configuration, connector.configuration_definition)
    df_test = connector.get_data(configuration, {}).toPandas()

    assert len(df_test.compare(df_sales)) == 0
    assert connector.executed_action == "./tests/.env/parquet/sales.parquet"

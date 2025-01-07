import os
import pandas as pd
from pyspark.sql import SparkSession
import pytest
from pyjeb import control_and_setup
from ploosh.engines.load_engine_spark import LoadEngineSpark
from ploosh.configuration import Configuration
from ploosh.connectors.connector_sql_spark import ConnectorSQLSpark

@pytest.fixture
def connector():
    # connection with hive metastore
    spark = SparkSession.builder \
        .appName("ploosh") \
        .master("spark://localhost:7077") \
        .config("spark.executor.memory", "1g") \
        .config("spark.driver.memory", "1g") \
        .config("spark.sql.warehouse.dir", f"{os.getcwd()}/spark-warehouse") \
        .enableHiveSupport() \
        .getOrCreate()
    
    connector = ConnectorSQLSpark()
    connector.spark = spark

    return connector

@pytest.fixture
def df_sales():
    return pd.read_csv("./tests/.data/sales.csv", delimiter=",", date_format = "%Y-%m-%d", parse_dates=["sale_date"])

#def test_get_data(connector, df_sales):
#    configuration = {
#        "query": "select * from sales;"
#    }
#    
#    connection = {}
#
#    df_test = connector.get_data(configuration, connection).toPandas()
#
#    assert len(df_test.compare(df_sales)) == 0
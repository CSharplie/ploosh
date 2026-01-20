import os
import pandas as pd
from pyspark.sql import SparkSession
import pytest
from pyjeb import control_and_setup
from ploosh.connectors.connector_json_spark import ConnectorJSONSpark

@pytest.fixture
def connector():
    spark = SparkSession.builder \
        .appName("ploosh") \
        .master("local[*]") \
        .config("spark.executor.memory", "1g") \
        .config("spark.driver.memory", "1g") \
        .getOrCreate()
    
    connector = ConnectorJSONSpark()
    connector.spark = spark

    return connector

@pytest.fixture
def df_sales():
    return pd.read_csv("./tests/.data/sales.csv", delimiter=",", date_format = "%Y-%m-%d", parse_dates=["sale_date"])

def test_default(connector, df_sales):
    configuration = {
       "path": f"{os.getcwd()}/tests/.env/json/sales.json",
    }

    configuration =  control_and_setup(configuration, connector.configuration_definition)

    df_test = connector.get_data(configuration, {}).toPandas()

    # Sort columns to ensure consistent order for comparison
    df_test = df_test.sort_index(axis=1)
    df_sales_sorted = df_sales.sort_index(axis=1)

    assert len(df_test.compare(df_sales_sorted)) == 0
    assert connector.executed_action == f"{os.getcwd()}/tests/.env/json/sales.json"


def test_multiline_false(connector, df_sales):
    configuration = {
       "path": f"{os.getcwd()}/tests/.env/json/sales.json",
       "multiline": False
    }

    configuration =  control_and_setup(configuration, connector.configuration_definition)

    df_test = connector.get_data(configuration, {}).toPandas()

    # Sort columns to ensure consistent order for comparison
    df_test = df_test.sort_index(axis=1)
    df_sales_sorted = df_sales.sort_index(axis=1)

    assert len(df_test.compare(df_sales_sorted)) == 0
    assert connector.executed_action == f"{os.getcwd()}/tests/.env/json/sales.json"


def test_encoding_iso88591(connector, df_sales):
    configuration = {
       "path": f"{os.getcwd()}/tests/.env/json/sales-ISO-8859-1.json",
       "encoding": "ISO-8859-1"
    }

    configuration =  control_and_setup(configuration, connector.configuration_definition)

    df_test = connector.get_data(configuration, {}).toPandas()

    # Sort columns to ensure consistent order for comparison
    df_test = df_test.sort_index(axis=1)
    df_sales_sorted = df_sales.sort_index(axis=1)

    assert len(df_test.compare(df_sales_sorted)) == 0
    assert connector.executed_action == f"{os.getcwd()}/tests/.env/json/sales-ISO-8859-1.json"
import os
import pandas as pd
from pyspark.sql import SparkSession
import pytest
from pyjeb import control_and_setup
from ploosh.engines.load_engine_spark import LoadEngineSpark
from ploosh.configuration import Configuration
from ploosh.connectors.connector_csv_spark import ConnectorCSVSpark

@pytest.fixture
def connector():
    spark = SparkSession.builder \
        .appName("ploosh") \
        .master("local[*]") \
        .config("spark.executor.memory", "1g") \
        .config("spark.driver.memory", "1g") \
        .getOrCreate()
    
    connector = ConnectorCSVSpark()
    connector.spark = spark

    return connector

@pytest.fixture
def df_sales():
    return pd.read_csv("./tests/.data/sales.csv", delimiter=",", dtype=object, date_format = "%Y-%m-%d", parse_dates=["sale_date"])

@pytest.fixture
def df_sales_with_types():
    return pd.read_csv("./tests/.data/sales.csv", delimiter=",", dtype={"sale_id": "int64", "product_id": "int64", "sale_amount": "float64"}, date_format = "%Y-%m-%d", parse_dates=["sale_date"])

def test_default(connector, df_sales):
    configuration = {
       "path": f"{os.getcwd()}/tests/.data/sales.csv",
    }

    configuration =  control_and_setup(configuration, connector.configuration_definition)

    df_test = connector.get_data(configuration, {}).toPandas()

    assert len(df_test.compare(df_sales)) == 0
    assert connector.executed_action == f"{os.getcwd()}/tests/.data/sales.csv"

def test_delimiter(connector, df_sales):
    configuration = {
       "path": f"{os.getcwd()}/tests/.env/csv/sales_with_tab.csv",
       "delimiter": "\t"
    }

    configuration =  control_and_setup(configuration, connector.configuration_definition)

    df_test = connector.get_data(configuration, {}).toPandas()

    assert len(df_test.compare(df_sales)) == 0
    assert connector.executed_action == f"{os.getcwd()}/tests/.env/csv/sales_with_tab.csv"

def test_infer_schema(connector, df_sales_with_types):
    configuration = {
       "path": f"{os.getcwd()}/tests/.data/sales.csv",
       "inferSchema": True
    }

    configuration =  control_and_setup(configuration, connector.configuration_definition)

    df_test = connector.get_data(configuration, {}).toPandas()

    assert len(df_test.compare(df_sales_with_types)) == 0
    assert connector.executed_action == f"{os.getcwd()}/tests/.data/sales.csv"

def test_quote(connector, df_sales):
    configuration = {
       "path": f"{os.getcwd()}/tests/.env/csv/sales_with_single_quote.csv",
       "quote": "'"
    }

    configuration =  control_and_setup(configuration, connector.configuration_definition)

    df_test = connector.get_data(configuration, {}).toPandas()

    assert len(df_test.compare(df_sales)) == 0
    assert connector.executed_action == f"{os.getcwd()}/tests/.env/csv/sales_with_single_quote.csv"

def test_encoding(connector, df_sales):
    configuration = {
       "path": f"{os.getcwd()}/tests/.env/csv/sales_with_iso_8859_1.csv",
       "encoding": "ISO-8859-1"
    }

    configuration =  control_and_setup(configuration, connector.configuration_definition)

    df_test = connector.get_data(configuration, {}).toPandas()

    assert len(df_test.compare(df_sales)) == 0
    assert connector.executed_action == f"{os.getcwd()}/tests/.env/csv/sales_with_iso_8859_1.csv"

def test_line_sep(connector, df_sales):
    configuration = {
       "path": f"{os.getcwd()}/tests/.env/csv/sales_with_cr.csv",
       "lineSep": "\r"
    }

    configuration =  control_and_setup(configuration, connector.configuration_definition)

    df_test = connector.get_data(configuration, {}).toPandas()

    assert len(df_test.compare(df_sales)) == 0
    assert connector.executed_action == f"{os.getcwd()}/tests/.env/csv/sales_with_cr.csv"

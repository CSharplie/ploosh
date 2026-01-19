import os
import pandas as pd
from pyspark.sql import SparkSession
import pytest
from pyjeb import control_and_setup
from delta import configure_spark_with_delta_pip
from ploosh.connectors.connector_delta_spark import ConnectorDeltaSpark

@pytest.fixture
def connector():
    spark = SparkSession.builder \
        .appName("ploosh") \
        .master("local[*]") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .config("spark.jars.packages", "io.delta:delta-spark_2.12:3.2.0") \
        .getOrCreate()
    
    connector = ConnectorDeltaSpark()
    connector.spark = spark

    return connector

@pytest.fixture
def df_sales():
    return pd.read_csv("./tests/.data/sales.csv", delimiter=",")

#def test_load_data(connector, df_sales):
#    configuration = {
#       "path": "./tests/.env/delta/sales"
#    }
#
#    configuration = control_and_setup(configuration, connector.configuration_definition)
#
#    df_test = connector.get_data(configuration, None).toPandas()
#
#    assert len(df_test.compare(df_sales)) == 0
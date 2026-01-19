import pytest
from pyspark.sql import SparkSession
from pyjeb import control_and_setup
from ploosh.connectors.connector_empty_spark import ConnectorEmptySpark

@pytest.fixture
def connector():
    spark = SparkSession.builder \
        .appName("ploosh") \
        .master("local[*]") \
        .config("spark.executor.memory", "1g") \
        .config("spark.driver.memory", "1g") \
        .getOrCreate()
    
    connector = ConnectorEmptySpark()
    connector.spark = spark

    return connector

def test_get_data(connector):
    configuration = {}
    connection = {}

    configuration = control_and_setup(configuration, connector.configuration_definition)
    connection = control_and_setup(connection, connector.connection_definition)

    df = connector.get_data(configuration, connection)

    assert df.count() == 0
    assert len(df.columns) == 0
    assert connector.executed_action == "empty"
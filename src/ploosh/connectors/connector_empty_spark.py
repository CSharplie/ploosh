# pylint: disable=R0903
"""Connector to return empty"""

from pyspark.sql.types import StructType
from connectors.connector import Connector


class ConnectorEmptySpark(Connector):
    """Connector to return empty"""

    def __init__(self):
        # Initialize the connector with its name and indicate it uses Spark
        self.name = "EMPTY_SPARK"
        self.is_spark = True
        self.connection_definition = []  # No specific connection parameters required
        self.configuration_definition = []  # No specific configuration parameters required

    def get_data(self, configuration: dict, connection: dict):
        """Return empty value"""

        # Create an empty RDD (Resilient Distributed Dataset)
        empty_rdd = self.spark.sparkContext.emptyRDD()

        # Define an empty schema (no columns)
        columns = StructType([])

        # Create an empty DataFrame using the empty RDD and schema
        df = self.spark.createDataFrame(data=empty_rdd, schema=columns)

        return df

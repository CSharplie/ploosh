# pylint: disable=R0903
"""Connector to read Delta table"""

from connectors.connector import Connector


class ConnectorDeltaSpark(Connector):
    """Connector to read Delta table with Spark"""

    def __init__(self):
        # Initialize the connector with its name and configuration definitions
        self.name = "DELTA_SPARK"
        self.is_spark = True  # Indicates that this connector uses Spark
        self.connection_definition = []  # No specific connection parameters required
        self.configuration_definition = [
            {"name": "path"},  # Path to the Delta table
        ]

    def get_data(self, configuration: dict, connection: dict):
        """Get data from source"""

        # Read the Delta table using Spark with the specified path
        df = self.spark.read.format("delta").load(configuration["path"])

        return df

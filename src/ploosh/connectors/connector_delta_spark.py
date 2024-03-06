# pylint: disable=R0903
"""Connector to read Delta table"""

from connectors.connector import Connector

class ConnectorDeltaSpark(Connector):
    """Connector to read Delta table with Spark"""
    def __init__(self):
        self.name = "DELTA_SPARK"
        self.is_spark = True
        self.connection_definition = []
        self.configuration_definition = [
            { "name": "path" },
        ]

    def get_data(self, configuration: dict, connection: dict):
        """Get data from source"""

        df = self.spark.read.format("delta").load(configuration["path"])

        return df

# pylint: disable=R0903
"""Connector to read CSV file"""

from connectors.connector import Connector

class ConnectorCSVSpark(Connector):
    """Connector to read CSV file with Spark"""
    def __init__(self):
        self.name = "CSV_SPARK"
        self.is_spark = True
        self.connection_definition = []
        self.configuration_definition = [
            { "name": "path" },
            { "name": "delimiter", "default": "," },
            { "name": "header", "type": "boolean", "default": True }
        ]

    def get_data(self, configuration: dict, connection: dict):
        """Get data from source"""

        df = self.spark.read \
            .option("delimiter", configuration["delimiter"]) \
            .option("header", configuration["header"]) \
            .csv(configuration["path"])

        return df

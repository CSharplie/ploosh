# pylint: disable=R0903
"""Connector to read CSV file"""

from connectors.connector import Connector


class ConnectorCSVSpark(Connector):
    """Connector to read CSV file with Spark"""

    def __init__(self):
        # Initialize the connector with its name and configuration definitions
        self.name = "CSV_SPARK"
        self.is_spark = True
        self.connection_definition = []
        self.configuration_definition = [
            {"name": "path"},  # Path to the CSV file
            {"name": "delimiter", "default": ","},  # Delimiter used in the CSV file
            {"name": "header", "type": "boolean", "default": True},  # Whether the CSV file has a header row
        ]

    def get_data(self, configuration: dict, connection: dict):
        """Get data from source"""

        # Read the CSV file using Spark with the specified configuration options
        df = (
            self.spark.read.option("delimiter", configuration["delimiter"])
            .option("header", configuration["header"])
            .csv(configuration["path"])
        )

        return df

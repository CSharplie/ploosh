# pylint: disable=R0903
"""Connector to read json file"""

from connectors.connector import Connector


class ConnectorJSONSpark(Connector):
    """Connector to read json file with Spark"""

    def __init__(self):
        # Initialize the connector with its name and configuration definitions
        self.name = "JSON_SPARK"
        self.is_spark = True
        self.connection_definition = []
        self.configuration_definition = [
            {"name": "path", "type": "string"},  # Path to the JSON file
            {"name": "multiline", "type": "boolean", "default": True},  # Handles multi-line JSON files
            {"name": "encoding", "type": "string", "default": "UTF-8"},  # Character encoding format used in the JSON file
            {"name": "lineSep", "type": "string", "default": "\n"}  # Character used to denote a line break
        ]

    def get_data(self, configuration: dict, connection: dict):
        """Get data from source"""

        # Read the JSON file using Spark with the specified configuration options
        df = self.spark.read.option("multiline", configuration["multiline"])    \
                            .option("encoding", configuration["encoding"])      \
                            .option("lineSep", configuration["lineSep"])        \
                            .json(configuration["path"])

        return df

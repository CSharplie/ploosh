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
            {"name": "path", "type": "string"},  # Path to the CSV file
            {"name": "delimiter", "type": "string", "default": ","},  # Delimiter used in the CSV file
            {"name": "header", "type": "boolean", "default": True},  # Whether the CSV file has a header row
            {"name": "inferSchema", "type": "boolean", "default": False},  # Infers the input schema automatically from data
            {"name": "multiline", "type": "boolean", "default": False},  # Parse one record, which may span multiple lines, per file
            {"name": "quote", "type": "string", "default": '"'},  # Character used to denote the start and end of a quoted item
            {"name": "encoding", "type": "string", "default": 'UTF-8'},  # Encoding to use for UTF when reading/writing
            {"name": "lineSep", "type": "string", "default": "\n"},  # Character used to denote a line break
        ]

    def get_data(self, configuration: dict, connection: dict):
        """Get data from source"""

        # Read the CSV file using Spark with the specified configuration options
        df = self.spark.read.option("delimiter", configuration["delimiter"])    \
                            .option("header", configuration["header"])          \
                            .option("inferSchema", configuration["inferSchema"])\
                            .option("multiline", configuration["multiline"])    \
                            .option("quote", configuration["quote"])            \
                            .option("encoding", configuration["encoding"])      \
                            .option("lineSep", configuration["lineSep"])        \
                            .csv(configuration["path"])

        return df

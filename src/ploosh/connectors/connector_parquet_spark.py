# pylint: disable=R0903
"""Connector to read Parquet file"""

import pandas as pd
from connectors.connector import Connector


class ConnectorParquetSpark(Connector):
    """Connector to read Parquet file"""

    def __init__(self):
        # Initialize the connector with its name and configuration definitions
        self.name = "PARQUET_SPARK"
        self.is_spark = True
        self.connection_definition = []  # No specific connection parameters required
        self.configuration_definition = [
            {"name": "path"}  # Path to the Parquet file
        ]

    def get_data(self, configuration: dict, connection: dict):
        """Get data from source"""

        # Extract the path and configuration parameters
        path = configuration["path"]

        # Read the Parquet file using pandas
        df = self.spark.read.parquet(path)

        return df

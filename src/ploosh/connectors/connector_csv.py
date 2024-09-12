# pylint: disable=R0903
"""Connector to read CSV file"""

import pandas as pd
from connectors.connector import Connector


class ConnectorCSV(Connector):
    """Connector to read CSV file"""

    def __init__(self):
        # Initialize the connector with its name and configuration definitions
        self.name = "CSV"
        self.connection_definition = []  # No specific connection parameters required
        self.configuration_definition = [
            {"name": "path"},  # Path to the CSV file
            {"name": "delimiter", "default": ","},  # Delimiter used in the CSV file
        ]

    def get_data(self, configuration: dict, connection: dict):
        """Get data from source"""

        # Extract the path and delimiter from the configuration
        path = configuration["path"]
        delimiter = configuration["delimiter"]

        # Read the CSV file using pandas with the specified delimiter
        df = pd.read_csv(path, delimiter=delimiter)
        return df
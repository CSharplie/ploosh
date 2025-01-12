# pylint: disable=R0903
"""Connector to read JSON file"""

import pandas as pd
from connectors.connector import Connector


class ConnectorJSON(Connector):
    """Connector to read JSON file"""

    def __init__(self):
        # Initialize the connector with its name and configuration definitions
        self.name = "JSON"
        self.connection_definition = []  # No specific connection parameters required
        self.configuration_definition = [
            {"name": "path"},  # Path to the JSON file
            {"name": "encoding", "type": "string", "default": "utf-8"},  # Encoding to use when reading the JSON file.
            {"name": "lines", "type": "boolean", "default": False},  # Whether to treat the file as line-delimited JSON (one JSON object per line).
            {"name": "nrows", "type": "integer", "default": None}  # Number of lines to read from a line-delimited JSON file.
        ]

    def get_data(self, configuration: dict, connection: dict):
        """Get data from source"""

        # Read the JSON file using pandas with the specified delimiter
        df = pd.read_json(configuration["path"],
                         encoding = configuration["encoding"],
                         lines = configuration["lines"],
                         nrows = configuration["nrows"]
                         )
        return df

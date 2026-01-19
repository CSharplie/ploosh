"""Connector to read Excel file"""

import pandas as pd
from connectors.connector import Connector


class ConnectorExcel(Connector):
    """Connector to read Excel file"""

    def __init__(self):
        # Initialize the connector with its name and configuration definitions
        self.name = "EXCEL"
        self.connection_definition = []  # No specific connection parameters required
        self.configuration_definition = [
            {"name": "path"},  # Path to the Excel file
            {"name": "sheet_name"},  # Sheet name
            {"name": "skiprows", "type": "integer", "default": 0},  # Number of rows to skip
        ]

    def get_data(self, configuration: dict, connection: dict):
        """Get data from source"""
        # Store the executed action (file path) for reference
        self.executed_action = configuration["path"]

        # Read the Excel file using pandas with the specified configuration options
        df = pd.read_excel(
            configuration["path"],
            sheet_name=configuration["sheet_name"],
            skiprows=configuration["skiprows"],
        )
        return df

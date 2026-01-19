# pylint: disable=R0903
"""Connector to read delta file"""

from deltalake import DeltaTable
from connectors.connector import Connector


class ConnectorDELTA(Connector):
    """Connector to read DELTA file"""

    def __init__(self):
        # Initialize the connector with its name and configuration definitions
        self.name = "DELTA"
        self.connection_definition = []  # No specific connection parameters required
        self.configuration_definition = [
            {"name": "path"}  # Path to the DELTA file
        ]

    def get_data(self, configuration: dict, connection: dict):
        """Get data from source"""

        # Store the executed action (file path) for reference
        self.executed_action = configuration["path"]

        # Read the DELTA file using pandas with the specified delimiter
        dt = DeltaTable(configuration["path"])
        df = dt.to_pandas()

        return df

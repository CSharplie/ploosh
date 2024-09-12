# pylint: disable=R0903
"""Connector to return empty"""

import pandas as pd
from connectors.connector import Connector


class ConnectorEmpty(Connector):
    """Connector to return empty"""

    def __init__(self):
        # Initialize the connector with its name and empty definitions
        self.name = "EMPTY"
        self.connection_definition = []  # No specific connection parameters required
        self.configuration_definition = []  # No specific configuration parameters required

    def get_data(self, configuration: dict, connection: dict):
        """Return empty value"""
        # Create an empty pandas DataFrame
        df = pd.DataFrame()
        return df

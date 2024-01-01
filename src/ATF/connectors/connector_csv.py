# pylint: disable=R0903
"""Connector to read CSV file"""

import pandas as pd
from connectors.connector import Connector

class ConnectorCSV(Connector):
    """Connector to read CSV file"""
    def __init__(self):
        self.name = "CSV"
        self.connection_definition = []
        self.configuration_definition = [{ "name": "path" }]

    def get_data(self, configuration: dict, connection: dict):
        """Get data from source"""

        path = configuration["path"]
        df = pd.read_csv(path)
        return df

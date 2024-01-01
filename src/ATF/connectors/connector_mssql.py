# pylint: disable=R0903
"""Connector to read MSSQL database"""

import pandas as pd
from connectors.connector import Connector

class ConnectorMSSQL(Connector):
    """Connector to read MSSQL database"""

    def __init__(self):
        self.name = "MSSQL"
        self.connection_definition = [
            {
                "name": "mode",
                "validset": ["connection_string", "password"],
                "default" : "connection_string"
            },
            {
                "name": "hostname",
                "default" : None
            },
            {
                "name": "database",
                "default" : None
            },
            {
                "name": "username",
                "default" : None
            },
            {
                "name": "password",
                "default" : None
            },
            {
                "name": "driver",
                "default" : "SQL Server"
            }
        ]
        self.configuration_definition = [{ "name": "query" }]

    def get_data(self, configuration: dict, connection: dict):
        """Get data from source"""

        path = configuration["path"]
        df = pd.read_csv(path)
        return df

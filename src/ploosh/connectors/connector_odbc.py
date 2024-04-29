# pylint: disable=R0903
"""Connector to read BigQuery database"""

import warnings
import pandas as pd
from sqlalchemy import create_engine
from connectors.connector import Connector

class ConnectorODCB(Connector):
    """Connector to read ODBC connection"""

    def __init__(self):
        self.name = "ODBC"
        self.connection_definition = [
            {
                "name": "DSN"
            },
            {
                "name": "auto_commit",
                "type": "boolean",
                "default": True,
            },
            {
                "name": "use_credentials",
                "type": "boolean",
                "default": False,
            },
            {
                "name": "user"
            },
            {
                "name": "password",
            },
        ]
        self.configuration_definition = [{ "name": "query" }, { "name": "connection" }]

    def get_data(self, configuration: dict, connection: dict):
        """Get data from source"""

        if connection["use_credentials"]:
            odbc_connection = pyodbc.connect(f"DSN={connection['DNS']}", user=connection["user"], password=connection["password"], autocommit=connection["auto_commit"])
        else:
            odbc_connection = pyodbc.connect(f"DSN={connection['DNS']}", autocommit=connection["auto_commit"])

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
          
            df = pd.read_sql(configuration["query"], odbc_connection)

        return df

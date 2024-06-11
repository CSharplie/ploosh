# pylint: disable=R0903
"""Connector to read ODBC connection"""

import warnings
import pandas as pd
import pyodbc
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
                "name": "user",
                "default": None,
            },
            {
                "name": "password",
                "default": None,
            },
            {
                "name": "encoding",
                "default": "UTF-8"
            }
        ]
        self.configuration_definition = [{ "name": "query" }, { "name": "connection" }]

    def get_data(self, configuration: dict, connection: dict):
        """Get data from source"""

        if connection["use_credentials"]:
            odbc_connection = pyodbc.connect(f"DSN={connection['DSN']}", user=connection["user"], password=connection["password"], autocommit=connection["auto_commit"])
        else:
            odbc_connection = pyodbc.connect(f"DSN={connection['DSN']}", autocommit=connection["auto_commit"])

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
          
            odbc_connection.setdecoding(pyodbc.SQL_CHAR, encoding=connection["encoding"])
            odbc_connection.setdecoding(pyodbc.SQL_WCHAR, encoding=connection["encoding"])
            odbc_connection.setencoding(encoding=connection["encoding"])

            df = pd.read_sql(configuration["query"], odbc_connection)

        return df

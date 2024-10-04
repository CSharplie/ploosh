# pylint: disable=R0903
"""Connector to read ODBC connection"""

import warnings
import pandas as pd
import pyodbc
from connectors.connector import Connector


class ConnectorODCB(Connector):
    """Connector to read ODBC connection"""

    def __init__(self):
        # Initialize the connector with its name and connection definitions
        self.name = "ODBC"
        self.connection_definition = [
            {
                "name": "mode",
                "default": "DSN",
                "validset": ["DSN", "connection_string"],
            },
            {
                "name": "DSN",  # Data Source Name for the ODBC connection
                "default": None
            },
            {
                "name": "connection_string",
                "default": None
            },
            {
                "name": "auto_commit",
                "type": "boolean",
                "default": True,  # Whether to enable auto-commit
            },
            {
                "name": "use_credentials",
                "type": "boolean",
                "default": False,  # Whether to use credentials for the connection
            },
            {
                "name": "user",
                "default": None,  # Username for the connection
            },
            {
                "name": "password",
                "default": None,  # Password for the connection
            },
            {
                "name": "encoding",
                "default": "UTF-8",  # Encoding to use for the connection
            },
        ]
        self.configuration_definition = [{"name": "query"}, {"name": "connection"}]

    def get_data(self, configuration: dict, connection: dict):
        """Get data from source"""

        if connection["mode"] == "DSN":
            # Establish the ODBC connection using the provided DSN and optional credentials
            if connection["use_credentials"]:
                odbc_connection = pyodbc.connect(
                    f"DSN={connection['DSN']}",
                    user=connection["user"],
                    password=connection["password"],
                    autocommit=connection["auto_commit"],
                )
            else:
                odbc_connection = pyodbc.connect(
                    f"DSN={connection['DSN']};", autocommit=connection["auto_commit"]
                )
        else:
            odbc_connection = pyodbc.connect(
                connection["connection_string"], autocommit=connection["auto_commit"]
            )

        # Suppress warnings related to encoding settings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)

            # Set the encoding for the ODBC connection
            odbc_connection.setdecoding(
                pyodbc.SQL_CHAR, encoding=connection["encoding"]
            )
            odbc_connection.setdecoding(
                pyodbc.SQL_WCHAR, encoding=connection["encoding"]
            )
            odbc_connection.setencoding(encoding=connection["encoding"])

            # Execute the SQL query and read the data into a pandas DataFrame
            df = pd.read_sql(configuration["query"], odbc_connection)

        return df

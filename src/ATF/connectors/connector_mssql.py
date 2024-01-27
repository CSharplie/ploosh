# pylint: disable=R0903
"""Connector to read MSSQL database"""

import pandas as pd
from sqlalchemy import create_engine
from connectors.connector import Connector

class ConnectorMSSQL(Connector):
    """Connector to read MSSQL database"""

    def __init__(self):
        self.name = "MSSQL"
        self.connection_definition = [
            {
                "name": "mode",
                "default" : "password",
                "validset": ["password", "connection_string"]
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
                "name":"port",
                "default": 1433,
                "type": "integer"
            },
            {
                "name":"driver",
                "default": "ODBC Driver 18 for SQL Server",
            },
            {
                "name":"connection_string",
                "default": None
            }
        ]
        self.configuration_definition = [{ "name": "query" }, { "name": "connection" }]

    def get_data(self, configuration: dict, connection: dict):
        """Get data from source"""

        connection_string = connection["connection_string"]
        if connection["mode"] == "password":
            driver = connection["driver"]
            port = connection["port"]
            hostname = connection["hostname"]
            username = connection["username"]
            password = connection["password"]
            database = connection["database"]

            connection_string = f"mssql+pyodbc://{username}:{password}@{hostname}:{port}/{database}?driver={driver}"

        sql_connection = create_engine(connection_string, echo=False)

        df = pd.read_sql(configuration["query"], sql_connection)

        return df

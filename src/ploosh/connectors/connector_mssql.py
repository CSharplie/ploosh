# pylint: disable=R0903
"""Connector to read MSSQL database"""

import pandas as pd
from sqlalchemy import create_engine
import urllib
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
                "name": "port",
                "default": 1433,
                "type": "integer"
            },
            {
                "name": "encrypt",
                "default": True,
                "type": "boolean"
            },
            {
                "name": "trust_server_certificate",
                "default": False,
                "type": "boolean"
            },
            {
                "name": "driver",
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
            trust_server_certificate = "yes" if connection["trust_server_certificate"] else "no"
            encrypt = "yes" if connection["encrypt"] else "no"

            odbc_connect = urllib.parse.quote_plus(f"Driver={driver};Server={hostname};Database={database};Uid={username};Pwd={password};Encrypt={encrypt};TrustServerCertificate={trust_server_certificate};")
            connection_string = f'mssql+pyodbc:///?odbc_connect={odbc_connect}'

        sql_connection = create_engine(connection_string, echo=False)

        df = pd.read_sql(configuration["query"], sql_connection)

        return df

# pylint: disable=R0903
"""Connector to read Databricks database"""

import pandas as pd
from sqlalchemy import create_engine
from connectors.connector import Connector

class ConnectorDatabricks(Connector):
    """Connector to read Databricks database"""

    def __init__(self):
        self.name = "DATABRICKS"
        self.connection_definition = [
            {
                "name": "token"
            },    
            {
                "name": "hostname"
            },
            {
                "name": "database"
            },
            {
                "name": "http_path"
            },
            {
                "name":"port",
                "default": 443,
                "type": "integer"
            }
        ]
        self.configuration_definition = [{ "name": "query" }, { "name": "connection" }]

    def get_data(self, configuration: dict, connection: dict):
        """Get data from source"""

        token = connection["token"]
        hostname = connection["hostname"]
        database = connection["database"]
        port = connection["port"]
        http_path = connection["http_path"]

        connection_string = f"databricks://token:{token}@{hostname}:{port}/{database}?http_path={http_path}"

        sql_connection = create_engine(connection_string, echo=False)

        df = pd.read_sql(configuration["query"], sql_connection)

        return df

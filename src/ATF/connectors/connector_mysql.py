# pylint: disable=R0903
"""Connector to read MYSQL database"""

import pandas as pd
import pymysql
from sqlalchemy import create_engine
from connectors.connector import Connector

class ConnectorMYSQL(Connector):
    """Connector to read MYSQL database"""

    def __init__(self):
        self.name = "MYSQL"
        self.connection_definition = [
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
                "default": 3306,
                "type": "integer"
            }
        ]
        self.configuration_definition = [{ "name": "query" }, { "name": "connection" }]

    def get_data(self, configuration: dict, connection: dict):
        """Get data from source"""

        port = connection["port"]
        hostname = connection["hostname"]
        username = connection["username"]
        password = connection["password"]
        database = connection["database"]

        cnx = create_engine(f"mysql+pymysql://{username}:{password}@{hostname}:{port}/{database}", echo=False)

        df = pd.read_sql(configuration["query"], cnx)

        return df

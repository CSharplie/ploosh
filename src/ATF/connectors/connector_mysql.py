# pylint: disable=R0903
"""Connector to read MYSQL database"""

import pandas as pd
from sqlalchemy import create_engine
from connectors.connector import Connector

class ConnectorMYSQL(Connector):
    """Connector to read MYSQL database"""

    def __init__(self):
        self.name = "MYSQL"
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
                "default": 3306,
                "type": "integer"
            },
            {
                "name":"require_secure_transport",
                "default": False,
                "type": "boolean"
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
            port = connection["port"]
            hostname = connection["hostname"]
            username = connection["username"]
            password = connection["password"]
            database = connection["database"]
            connection_string = f"mysql+pymysql://{username}:{password}@{hostname}:{port}/{database}"


        connect_args = {}
        if connection["require_secure_transport"] :
            connect_args = {'ssl':{'require_secure_transport': True}}

        sql_connection = create_engine(connection_string, echo=False, connect_args=connect_args)

        df = pd.read_sql(configuration["query"], sql_connection)

        return df

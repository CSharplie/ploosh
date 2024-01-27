# pylint: disable=R0903
"""Connector to read Snowflake database"""

import pandas as pd
from sqlalchemy import create_engine
from connectors.connector import Connector

class ConnectorSnowflake(Connector):
    """Connector to read Snowflake database"""

    def __init__(self):
        self.name = "SNOWFLAKE"
        self.connection_definition = [
            {
                "name": "account_identifier"
            },
            {
                "name": "username"
            },
            {
                "name": "password"
            },
            {
                "name": "database",
                "default": None
            },
            {
                "name": "schema",
                "default": None
            },
            {
                "name": "warehouse",
                "default": None
            },
            {
                "name": "role",
                "default": None
            }
        ]
        self.configuration_definition = [{ "name": "query" }, { "name": "connection" }]

    def get_data(self, configuration: dict, connection: dict):
        """Get data from source"""


        account_identifier = connection["account_identifier"]
        username = connection["username"]
        password = connection["password"]
        connection_string = f"snowflake://{username}:{password}@{account_identifier}/"


        if connection["database"] is not None: connection_string += f"{connection['database']}/"
        if connection["schema"] is not None: connection_string += f"{connection['schema']}"

        connection_string += "?1=1"

        if connection["warehouse"] is not None: connection_string += f"&warehouse={connection['warehouse']}"
        if connection["role"] is not None: connection_string += f"&role={connection['role']}"

        sql_connection = create_engine(connection_string, echo=False)

        df = pd.read_sql(configuration["query"], sql_connection)

        return df

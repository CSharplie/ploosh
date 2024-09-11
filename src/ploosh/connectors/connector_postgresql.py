# pylint: disable=R0903
"""Connector to read PostgreSQL database"""

import pandas as pd
from sqlalchemy import create_engine
from connectors.connector import Connector


class ConnectorPostgreSQL(Connector):
    """Connector to read PostgreSQL database"""

    def __init__(self):
        # Initialize the connector with its name and connection definitions
        self.name = "POSTGRESQL"
        self.connection_definition = [
            {
                "name": "mode",
                "default": "password",
                "validset": ["password", "connection_string"],
            },
            {
                "name": "hostname",
                "default": None,
            },
            {
                "name": "database",
                "default": None,
            },
            {
                "name": "username",
                "default": None,
            },
            {
                "name": "password",
                "default": None,
            },
            {
                "name": "port",
                "default": 5432,
                "type": "integer",
            },
            {
                "name": "ssl_context",
                "default": False,
                "type": "boolean",
            },
            {
                "name": "connection_string",
                "default": None,
            },
        ]
        self.configuration_definition = [{"name": "query"}, {"name": "connection"}]

    def get_data(self, configuration: dict, connection: dict):
        """Get data from source"""

        # Use the provided connection string if mode is "connection_string"
        connection_string = connection["connection_string"]
        if connection["mode"] == "password":
            # Extract connection parameters
            port = connection["port"]
            hostname = connection["hostname"]
            username = connection["username"]
            password = connection["password"]
            database = connection["database"]
            # Create the connection string for PostgreSQL
            connection_string = (
                f"postgresql+pg8000://{username}:{password}@{hostname}:{port}/{database}"
            )

        # Additional connection arguments
        connect_args = {}
        if connection["ssl_context"]:
            connect_args = {"ssl_context": True}

        # Create a SQLAlchemy engine using the connection string and additional arguments
        sql_connection = create_engine(
            connection_string, echo=False, connect_args=connect_args
        )

        # Execute the SQL query and read the data into a pandas DataFrame
        df = pd.read_sql(configuration["query"], sql_connection)

        return df

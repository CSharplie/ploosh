# pylint: disable=R0903
"""Connector to read MYSQL database"""

import pandas as pd
from sqlalchemy import create_engine
from connectors.connector import Connector


class ConnectorMYSQL(Connector):
    """Connector to read MYSQL database"""

    def __init__(self):
        # Initialize the connector with its name and connection definitions
        self.name = "MYSQL"
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
                "default": 3306,
                "type": "integer",
            },
            {
                "name": "require_secure_transport",
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
            # Create the connection string for MySQL
            connection_string = (
                f"mysql+pymysql://{username}:{password}@{hostname}:{port}/{database}"
            )

        # Additional connection arguments
        connect_args = {}
        if connection["require_secure_transport"]:
            connect_args = {"ssl": {"require_secure_transport": True}}

        # Create a SQLAlchemy engine using the connection string and additional arguments
        sql_connection = create_engine(
            connection_string, echo=False, connect_args=connect_args
        )

        # Execute the SQL query and read the data into a pandas DataFrame
        df = pd.read_sql(configuration["query"], sql_connection)

        return df

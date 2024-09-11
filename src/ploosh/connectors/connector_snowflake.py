# pylint: disable=R0903
"""Connector to read Snowflake database"""

import pandas as pd
from sqlalchemy import create_engine
from connectors.connector import Connector


class ConnectorSnowflake(Connector):
    """Connector to read Snowflake database"""

    def __init__(self):
        # Initialize the connector with its name and connection definitions
        self.name = "SNOWFLAKE"
        self.connection_definition = [
            {
                "name": "account_identifier",  # Snowflake account identifier
            },
            {
                "name": "username",  # Username for authentication
            },
            {
                "name": "password",  # Password for authentication
            },
            {
                "name": "database",  # Database name (optional)
                "default": None,
            },
            {
                "name": "schema",  # Schema name (optional)
                "default": None,
            },
            {
                "name": "warehouse",  # Warehouse name (optional)
                "default": None,
            },
            {
                "name": "role",  # Role name (optional)
                "default": None,
            },
        ]
        self.configuration_definition = [{"name": "query"}, {"name": "connection"}]

    def get_data(self, configuration: dict, connection: dict):
        """Get data from source"""

        # Extract connection parameters
        account_identifier = connection["account_identifier"]
        username = connection["username"]
        password = connection["password"]

        # Create the base connection string for Snowflake
        connection_string = f"snowflake://{username}:{password}@{account_identifier}/"

        # Append database and schema to the connection string if provided
        if connection["database"] is not None:
            connection_string += f"{connection['database']}/"
        if connection["schema"] is not None:
            connection_string += f"{connection['schema']}"

        # Add query parameters to the connection string
        connection_string += "?1=1"
        if connection["warehouse"] is not None:
            connection_string += f"&warehouse={connection['warehouse']}"
        if connection["role"] is not None:
            connection_string += f"&role={connection['role']}"

        # Create a SQLAlchemy engine using the connection string
        sql_connection = create_engine(connection_string, echo=False)

        # Execute the SQL query and read the data into a pandas DataFrame
        df = pd.read_sql(configuration["query"], sql_connection)

        return df

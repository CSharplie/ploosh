# pylint: disable=R0903
"""Connector to read Databricks database"""

import pandas as pd
from sqlalchemy import create_engine
from connectors.connector import Connector


class ConnectorDatabricks(Connector):
    """Connector to read Databricks database"""

    def __init__(self):
        # Initialize the connector with its name and connection definitions
        self.name = "DATABRICKS"
        self.connection_definition = [
            {
                "name": "token",  # Token for authentication
            },
            {
                "name": "hostname",  # Hostname of the Databricks instance
            },
            {
                "name": "database",  # Database name
            },
            {
                "name": "http_path",  # HTTP path for the Databricks cluster
            },
            {
                "name": "port",  # Port number (default is 443)
                "default": 443,
                "type": "integer",
            },
        ]
        self.configuration_definition = [
            {"name": "query"},  # SQL query to execute
            {"name": "connection"},  # Connection name
        ]

    def get_data(self, configuration: dict, connection: dict):
        """Get data from source"""

        # Extract connection parameters
        token = connection["token"]
        hostname = connection["hostname"]
        database = connection["database"]
        port = connection["port"]
        http_path = connection["http_path"]

        # Create the connection string for Databricks
        connection_string = (
            f"databricks://token:{token}@{hostname}:{port}/{database}?http_path={http_path}"
        )

        # Create a SQLAlchemy engine using the connection string
        sql_connection = create_engine(connection_string, echo=False)

        # Execute the SQL query and read the data into a pandas DataFrame
        df = pd.read_sql(configuration["query"], sql_connection)

        return df

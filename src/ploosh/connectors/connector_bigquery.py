# pylint: disable=R0903
"""Connector to read BigQuery database"""

import pandas as pd
import pandas_gbq
from sqlalchemy import create_engine
from connectors.connector import Connector


class ConnectorBigQuery(Connector):
    """Connector to read BigQuery database"""

    def __init__(self):
        # Initialize the connector with its name and connection definitions
        self.name = "BIGQUERY"
        self.connection_definition = [
            {
                "name": "credentials",  # Credentials for authentication
                "default": None,
            },
            {
                "name": "credentials_type",  # Type of credentials (service account or current user)
                "validset": ["service_account", "current_user"],
                "default": "service_account",
            },
            {
                "name": "project_id",  # Project ID for BigQuery
                "default": None,
            },
        ]
        self.configuration_definition = [
            {"name": "query"},  # SQL query to execute
            {"name": "connection"},  # Connection name
        ]

    def get_data(self, configuration: dict, connection: dict):
        """Get data from source"""
        # Extract credentials and credentials type from the connection
        credentials = connection["credentials"]
        credentials_type = connection["credentials_type"]

        # If using service account credentials, create a connection string and use SQLAlchemy
        if credentials_type == "service_account":
            connection_string = f"bigquery://?credentials_base64={credentials}"
            sql_connection = create_engine(connection_string, echo=False)
            df = pd.read_sql(configuration["query"], sql_connection)
        # If using current user credentials, use pandas_gbq to read the data
        elif credentials_type == "current_user":
            df = pandas_gbq.read_gbq(
                configuration["query"], connection["project_id"], progress_bar_type=None
            )

        return df

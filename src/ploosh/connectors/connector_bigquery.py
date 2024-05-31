# pylint: disable=R0903
"""Connector to read BigQuery database"""

import pandas as pd
import pandas_gbq
from sqlalchemy import create_engine
from connectors.connector import Connector

class ConnectorBigQuery(Connector):
    """Connector to read BigQuery database"""

    def __init__(self):
        self.name = "BIGQUERY"
        self.connection_definition = [
            {
                "name": "credentials",
                "default": None
            },
            {
                "name": "credentials_type",
                "validset": ["service_account", "current_user"],
                "default": "service_account"
            },
            {
                "name": "project_id",
                "default": None
            }
        ]
        self.configuration_definition = [
            { "name": "query" }
            , { "name": "connection" }
        ]

    def get_data(self, configuration: dict, connection: dict):
        """Get data from source"""
        credentials = connection["credentials"]
        credentials_type = connection["credentials_type"]

        if credentials_type == "service_account":
            connection_string = f"bigquery://?credentials_base64={credentials}"
            sql_connection = create_engine(connection_string, echo=False)
            df = pd.read_sql(configuration["query"], sql_connection)
        elif credentials_type == "current_user":
            df = pandas_gbq.read_gbq(configuration["query"], connection["project_id"], progress_bar_type = None)

        return df

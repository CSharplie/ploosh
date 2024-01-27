# pylint: disable=R0903
"""Connector to read BigQuery database"""

import pandas as pd
from sqlalchemy import create_engine
from connectors.connector import Connector

class ConnectorBigQuery(Connector):
    """Connector to read BigQuery database"""

    def __init__(self):
        self.name = "BIGQUERY"
        self.connection_definition = [
            {
                "name": "credentials"
            },
        ]
        self.configuration_definition = [{ "name": "query" }, { "name": "connection" }]

    def get_data(self, configuration: dict, connection: dict):
        """Get data from source"""

        credentials = connection["credentials"]
        connection_string = f"bigquery://?credentials_base64={credentials}"

        sql_connection = create_engine(connection_string, echo=False)

        df = pd.read_sql(configuration["query"], sql_connection)

        return df

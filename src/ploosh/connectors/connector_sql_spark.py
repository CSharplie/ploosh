# pylint: disable=R0903
"""Connector to read SQL file"""

from connectors.connector import Connector

class ConnectorSQLSpark(Connector):
    """Connector to execute SQL query over Spark"""
    def __init__(self):
        self.name = "SQL_SPARK"
        self.is_spark = True
        self.connection_definition = []
        self.configuration_definition = [
            { "name": "query" }
        ]

    def get_data(self, configuration: dict, connection: dict):
        """Get data from source"""

        df = self.spark.sql(configuration["query"])

        return df

# pylint: disable=R0903
"""Connector to read SQL file"""

from connectors.connector import Connector


class ConnectorSQLSpark(Connector):
    """Connector to execute SQL query over Spark"""

    def __init__(self):
        # Initialize the connector with its name and indicate it uses Spark
        self.name = "SQL_SPARK"
        self.is_spark = True
        self.connection_definition = []  # No specific connection parameters required
        self.configuration_definition = [
            {"name": "query"}  # SQL query to execute
        ]

    def get_data(self, configuration: dict, connection: dict):
        """Get data from source"""

        # Execute the SQL query using Spark and return the resulting DataFrame
        df = self.spark.sql(configuration["query"])

        return df

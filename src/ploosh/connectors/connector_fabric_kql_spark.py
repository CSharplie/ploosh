# pylint: disable=R0903
"""Connector to read Fabric KQL data with Spark"""

from connectors.connector import Connector


class ConnectorFabricKqlSpark(Connector):
    """Connector to read Fabric KQL data with Spark"""

    def __init__(self):
        # Initialize the connector with its name and configuration definitions
        self.name = "FABRIC_KQL_SPARK"
        self.is_spark = True  # Indicates that this connector uses Spark
        self.connection_definition = [
            {
                "name": "kusto_uri", # Kusto cluster URI
            },
            {
                "name": "database_id", # KQL Database ID
            }
            ]
        self.configuration_definition = [
            {"name": "query"},  # KQL query to execute
        ]

    def get_data(self, configuration: dict, connection: dict):
        """Get data from source"""

        from notebookutils import mssparkutils

        accessToken = mssparkutils.credentials.getToken("kusto")

        # Read the KQL data using Spark with the specified connection and configuration options
        df = self.spark.read \
            .format("com.microsoft.kusto.spark.datasource") \
            .option("kustoCluster", connection["kusto_uri"]) \
            .option("kustoDatabase", connection["database_id"]) \
            .option("kustoQuery", configuration["query"]) \
            .option("accessToken", accessToken) \
            .load()

        return df

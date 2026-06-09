# pylint: disable=R0903,C0415,C0103
"""Connector to read Fabric KQL data with Spark"""
import requests
import pandas as pd

from connectors.connector import Connector


class ConnectorFabricKqlSpark(Connector):
    """Connector to read Fabric KQL data with Spark"""

    def __init__(self):
        # Initialize the connector with its name and configuration definitions
        self.name = "FABRIC_KQL_SPARK"
        self.is_spark = True  # Indicates that this connector uses Spark
        self.connection_definition = [
            {
                "name": "connection_mode",
                "validset": ["native", "api"],
                "default": "api"
            },
            {
                "name": "kusto_uri", # Kusto cluster URI
            },
            {
                "name": "database_id", # KQL Database ID
            },
            {
                "name": "database_name", # KQL Database Name
                "default": None
            }
            ]
        self.configuration_definition = [
            {"name": "query"},  # KQL query to execute
        ]

    def get_data(self, configuration: dict, connection: dict):
        """Get data from source"""

        from notebookutils import mssparkutils

        access_token = mssparkutils.credentials.getToken("kusto")

        # Store the executed query for reference
        self.executed_action = configuration["query"]

        if connection["connection_mode"] == "native":
            # Read the KQL data using Spark with the specified connection and configuration options
            df = self.spark.read \
                .format("com.microsoft.kusto.spark.datasource") \
                .option("kustoCluster", connection["kusto_uri"]) \
                .option("kustoDatabase", connection["database_id"]) \
                .option("kustoQuery", configuration["query"]) \
                .option("accessToken", access_token) \
                .load()
        else:
            url = f"{connection['kusto_uri'].rstrip('/')}/v2/rest/query"
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            payload = {
                "db": connection["database_name"],
                "csl": configuration["query"]
            }

            response = requests.post(url, json=payload, headers=headers)

            if response.status_code == 200:
                json_data = response.json()

                data_table = None
                for table in json_data:
                    if table.get("TableKind") == "PrimaryResult":
                        data_table = table
                        break

                    elif table.get("FrameType") == "DataTable" and table.get("TableRole") == "PrimaryResult":
                        data_table = table
                        break

                if data_table:
                    columns = [col["ColumnName"] for col in data_table["Columns"]]
                    rows = data_table["Rows"]

                    df = pd.DataFrame(rows, columns=columns)
                    df = self.spark.createDataFrame(df)
                else:
                    raise ValueError(
                        "Fabric KQL API response does not contain a PrimaryResult table."
                    )
            else:
                raise ValueError(
                    f"Fabric KQL API request failed with status {response.status_code}: {response.text}"
                )

        if df is None:
            raise ValueError("Fabric KQL connector returned no dataframe.")

        return df

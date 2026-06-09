# pylint: disable=R0903,C0415,C0103
"""Connector to read Fabric Warehouse data with Spark"""

from connectors.connector import Connector


class ConnectorFabricWarehouseSpark(Connector):
    """Connector to read Fabric Warehouse data with Spark"""

    def __init__(self):
        # Initialize the connector with its name and configuration definitions
        self.name = "FABRIC_WAREHOUSE_SPARK"
        self.is_spark = True  # Indicates that this connector uses Spark
        self.connection_definition = [
                {
                    "name": "warehouse_name",
                },
                {
                    "name": "workspace_name",
                    "default" : None
                }
            ]
        self.configuration_definition = [
            {"name": "query"},  # Warehouse query to execute
        ]

    def get_data(self, configuration: dict, connection: dict):
        """Get data from source"""

        from sempy_labs import ConnectWarehouse

        with ConnectWarehouse(warehouse=connection["warehouse_name"], workspace=connection["workspace_name"]) as sql:
            df_pandas = sql.query(configuration["query"])
            df = self.spark.createDataFrame(df_pandas)
            return df

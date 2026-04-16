# pylint: disable=R0903,C0415,C0103
"""Connector to read Dremio data with Spark"""

from connectors.connector import Connector


class ConnectorFabricSemanticModel(Connector):
    """Connector to read Fabric KQL data with Spark"""

    def __init__(self):
        # Initialize the connector with its name and configuration definitions
        self.name = "FABRIC_SEMANTIC_MODEL_SPARK"
        self.is_spark = True  # Indicates that this connector uses Spark
        self.connection_definition = [
            {
                "name": "semantic_model_name",
            },
            {
                "name": "workspace_name",
                "default": None
            }
        ]
        self.configuration_definition = [
            {
                "name": "method", 
                "validset": ["DAX Query", "Table", "Measure"]
            },
            {
                "name": "dax_query",
                "default": None
            },
            {
                "name": "table_to_query",
                "default": None
            },
            {
                "name": "measure_to_query",
                "default": None
            },
            {
                "name": "group_by", # example ["'Table Name'[Col name]", "'Table Name2'[Col name2]"]
                "type": "list",
                "default": None
            },
            {
                "name": "filters_to_apply", # example { " 'Table Name'[col name]" : ['val1', 'val2']}
                "type": "dict",
                "default": None
            },
            {   
                "name": "column_names",
                "type": "list"
            }
        ]

    def get_data(self, configuration: dict, connection: dict):
        """ Get data from Semantic Model using Spark based on the provided configuration and connection details."""

        from sempy import fabric

        workspace_name = connection['workspace_name']
        semantic_model_name = connection['semantic_model_name']

        method = configuration['method']

        # Returns explicit Workspace doesn't exist error
        df_datasets = fabric.list_datasets(workspace=workspace_name)

        # Returns explicit message if semantic model not found
        if semantic_model_name not in df_datasets['Dataset Name'].values:
            raise Exception(f"Semantic model '{semantic_model_name}' doesn't exist")

        if method == 'DAX Query':
            # Dax Query execution
            df = fabric.evaluate_dax(semantic_model_name, configuration['dax_query'], workspace=workspace_name)

        elif method == 'Table':
            df = fabric.read_table(semantic_model_name, configuration['table_to_query'], workspace=workspace_name)

        elif method == 'Measure':
            df_measures = fabric.list_measures(semantic_model_name, workspace=workspace_name)

            # Returns explicit message if measure not found
            if configuration['measure_to_query'] not in df_measures['Measure Name'].values:
                raise Exception(f"Measure '{configuration['measure_to_query']}' doesn't exist")

            df = fabric.evaluate_measure(
                semantic_model_name,
                configuration['measure_to_query'],
                configuration['group_by'],
                filters=configuration['filters_to_apply'],
                workspace=workspace_name,
            )

        else:
            raise Exception(f"Method '{method}' not recognized")

        column_names = configuration.get('column_names')
        if column_names:
            if len(column_names) != len(df.columns):
                raise Exception(
                    f"column_names has {len(column_names)} items but dataframe has {len(df.columns)} columns"
                )
            df.columns = column_names

        return self.spark.createDataFrame(df)

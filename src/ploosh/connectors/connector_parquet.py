# pylint: disable=R0903
"""Connector to read Parquet file"""

import pandas as pd
from connectors.connector import Connector


class ConnectorParquet(Connector):
    """Connector to read Parquet file"""

    def __init__(self):
        # Initialize the connector with its name and configuration definitions
        self.name = "PARQUET"
        self.connection_definition = []  # No specific connection parameters required
        self.configuration_definition = [
            {"name": "path"},  # Path to the Parquet file
            {"name": "columns", "type": "list", "default": None},  # Subset of columns to load
            {"name": "engine", "type": "string", "validset": ["auto", "pyarrow", "fastparquet"], "default": "auto"},  # Parquet engine to use ('auto', 'pyarrow', 'fastparquet')
            {"name": "filters", "type": "list", "default": None},  # Row group filters to apply (for 'pyarrow')
            {"name": "filters.column", "type": "string"},  # The name of the column to filter
            {"name": "filters.operator", "type": "string", "validset": ["==", "=", ">", ">=", "<", "<=", "!="]},  # The operator to be used
            {"name": "filters.value", "type": "integer"},  # The value to be used to filter the column
        ]

    def get_data(self, configuration: dict, connection: dict):
        """Get data from source"""

        # Extract the path and configuration parameters
        path = configuration["path"]
        columns = configuration["columns"]
        engine = configuration["engine"]
        filters = configuration["filters"]
        list_filters = None
        if filters is not None:
            list_filters = (
                [(filter_spec["column"], filter_spec["operator"], filter_spec["value"]) for filter_spec in filters]
                if filters else None
            )

        # Store the executed action (file path) for reference
        self.executed_action = path

        # Read the Parquet file using pandas
        df = pd.read_parquet(path,
                             columns=columns,
                             engine=engine,
                             filters=list_filters)
        return df

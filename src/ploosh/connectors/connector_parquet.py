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
            {"name": "engine", "type": "string", "default": "auto"},  # Parquet engine to use ('auto', 'pyarrow', 'fastparquet')
            {"name": "filters", "type": "list", "default": None},  # Row group filters to apply (for 'pyarrow')
        ]

    def get_data(self, configuration: dict, connection: dict):
        """Get data from source"""

        # Extract the path and configuration parameters
        path = configuration["path"]
        columns = configuration["columns"]
        engine = configuration["engine"]
        filters = configuration["filters"]

        # Check if the variable is a list
        if not isinstance(filters, list):
            raise ValueError("The variable must be a list.")

        # Check if the list is empty
        if not filters:
            raise ValueError("The list must not be empty.")

        # Check and convert each element into a tuple
        check_filters = []
        for element in filters:
            if not isinstance(element, list) or len(element) != 3:
                raise ValueError(
                    "Each element of the list must be a list containing exactly 3 elements: [column, op, val]."
                )
            # Convert the element into a tuple
            check_filters.append(tuple(element))

        # Read the Parquet file using pandas
        df = pd.read_parquet(path,
                             columns = columns,
                             engine  = engine,
                             filters = filters)
        return df

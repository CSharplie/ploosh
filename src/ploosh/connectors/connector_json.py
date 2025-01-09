# pylint: disable=R0903
"""Connector to read JSON file"""

import json
import pandas as pd
from connectors.connector import Connector


class ConnectorJSON(Connector):
    """Connector to read JSON file"""

    def __init__(self):
        # Initialize the connector with its name and configuration definitions
        self.name = "JSON"
        self.connection_definition = []  # No specific connection parameters required
        self.configuration_definition = [
            {"name": "path"},  # Path to the CSV file
            {"name": "dtype", "type": "boolean", "default": None},  #  infer dtypes
            {"name": "encoding", "type": "string", "default": "utf-8"},  # Encoding to use for UTF when reading/writing.
            {"name": "lines", "type": "boolean", "default": False},  # Read the file as a json object per line.
            {"name": "nrows", "type": "integer", "default": None}  # number of lines from the line-delimited jsonfile that has to be read.
        ]

    def get_data(self, configuration: dict, connection: dict):
        """Get data from source"""

        # Extract the path and delimiter from the configuration
        path = configuration["path"]
        dtype = configuration["dtype"]
        encoding = configuration["encoding"]
        lines = configuration["lines"]
        nrows = configuration["nrows"]

        # Read the CSV file using pandas with the specified delimiter
        df = pd.read_csv(path,
                         delimiter=delimiter,
                         header=header,
                         names=names,
                         usecols=usecols,
                         skiprows=skiprows,
                         skipfooter=skipfooter,
                         nrows=nrows,
                         lineterminator=lineterminator,
                         quotechar=quotechar,
                         engine=engine,
                         encoding=encoding)
        return df
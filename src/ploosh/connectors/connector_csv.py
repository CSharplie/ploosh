# pylint: disable=R0903
"""Connector to read CSV file"""

import json
import pandas as pd
from connectors.connector import Connector


class ConnectorCSV(Connector):
    """Connector to read CSV file"""

    def __init__(self):
        # Initialize the connector with its name and configuration definitions
        self.name = "CSV"
        self.connection_definition = []  # No specific connection parameters required
        self.configuration_definition = [
            {"name": "path"},  # Path to the CSV file
            {"name": "delimiter", "default": ","},  # Delimiter used in the CSV file
            {"name": "infer", "type": "boolean", "default": True},  # Infer the column names
            {"name": "names", "type": "list", "default": None},  # Sequence of column labels to apply
            {"name": "usecols", "type": "list", "default": None},  # Subset of columns to select
            {"name": "skiprows", "type": "string", "default": None},  # Line numbers to skip (0-indexed) or number of lines to skip (int) at the start of the file
            {"name": "skipfooter", "type": "integer", "default": 0},  # Number of lines at bottom of file to skip (Unsupported with engine='c')
            {"name": "nrows", "type": "integer", "default": None},  # Number of rows of file to read. Useful for reading pieces of large files.
            {"name": "lineterminator", "type": "string", "default": None},  # Character used to denote a line break.
            {"name": "quotechar", "type": "string", "default": '"'},  # Character used to denote the start and end of a quoted item.
            {"name": "encoding", "type": "string", "default": "utf-8"},  # Encoding to use for UTF when reading/writing.
            {"name": "engine", "type": "string", "default": None},  # Parser engine to use.
        ]

    def get_data(self, configuration: dict, connection: dict):
        """Get data from source"""

        # Extract the path and delimiter from the configuration
        path = configuration["path"]
        delimiter = configuration["delimiter"]
        header = None if configuration["infer"] is False else "infer"
        names = configuration["names"]
        usecols = configuration["usecols"]
        skiprows = None
        skipfooter = configuration["skipfooter"]
        nrows = configuration["nrows"]
        lineterminator = configuration["lineterminator"]
        quotechar = configuration["quotechar"]
        encoding = configuration["encoding"]
        engine = configuration["engine"]

        if configuration["skiprows"] is not None:
            try:
                skiprows = json.loads(configuration["skiprows"])
            except json.JSONDecodeError:
                raise ValueError("The variable is neither a list nor an integer.")

        if skiprows is not None and not isinstance(skiprows, (list, int)):
            raise ValueError("The variable is neither a list nor an integer.")

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
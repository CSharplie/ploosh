# pylint: disable=R0903
"""Connector to return empty"""

import pandas as pd
from connectors.connector import Connector

class ConnectorEmpty(Connector):
    """Connector to return empty"""
    def __init__(self):
        self.name = "EMPTY_SPARK"
        self.is_spark = True
        self.connection_definition = []
        self.configuration_definition = []

    def get_data(self, configuration: dict, connection: dict):
        """Return empty value"""
        df = self.spark.emptyDataFrame
        return df

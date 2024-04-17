# pylint: disable=R0903
"""Connector to return empty"""

import pandas as pd
from pyspark.sql.types import StructType
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
        empty_RDD = self.spark.sparkContext.emptyRDD()
        columns = StructType([])
        df = self.spark.createDataFrame(data = empty_RDD, schema = columns)

        return df

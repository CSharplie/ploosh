import numpy as np
import pandas as pd

from engines.load_engine import LoadEngine

class LoadEngineSpark(LoadEngine):
    def __init__(self, configuration, options, connection):
        self.configuration = configuration
        self.options = options
        self.connection = connection

    def execute(self, df_data):
        self.count = df_data.count()

        # TODO: Implement Spark specific data transformations

        return df_data

import numpy as np
import pandas as pd

from engines.load_engine import LoadEngine

class LoadEngineNative(LoadEngine):
    def __init__(self, configuration, options, connection):
        self.configuration = configuration
        self.options = options
        self.connection = connection

    def execute(self, df_data):
        self.count = len(df_data)

        # Cast columns to specified types
        for column in self.options["cast"]:
            column_name = self.get_insensitive_item(column["name"], df_data.columns)
            column_type = column["type"]
            if column_type == "datetime":
                column_type = "datetime64[ns]"
            df_data[column_name] = df_data[column_name].astype(column_type, errors="ignore")

        # Remap bad columns type
        for column in df_data.select_dtypes(include=["object"]).columns:
            if len(df_data) == 0:
                continue

            if type(df_data[column][0]).__name__ == "Decimal":
                df_data[column] = df_data[column].astype(float, errors="ignore")

        # Remove time zones
        date_columns = df_data.select_dtypes(include=["datetime64[ns, UTC]"]).columns
        for date_column in date_columns:
            df_data[date_column] = df_data[date_column].dt.tz_localize(None)
        self.count = len(df_data)

        return df_data

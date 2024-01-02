"""Module to manage test case"""
from dataclasses import dataclass
from datetime import datetime
import numpy as np
import pandas as pd

@dataclass
class ConnectionDescription:
    """Tuple of connection and connector"""
    connector = None
    connection = None

    def __init__(self, connector, connection):
        self.connector = connector
        self.connection = connection

@dataclass
class Duration:
    """Structure of duration"""

    start = None
    end = None
    duration = None

    def calculate_duration(self):
        """Calculate the duration between start and end date"""
        if self.end is not None:
            self.duration = (self.end - self.start).microseconds / 60000000

@dataclass
class CaseItem:
    """Structure of case item (source or expected)"""

    connector = None
    connection = None
    configuration = None

    duration = Duration()

    df_data = None

    def __init__(self, configuration, connector, connection):
        self.connector = connector
        self.connection = connection
        self.configuration = configuration

class Case:
    """Test case item"""

    source = None
    expected = None

    global_duration = Duration()
    compare_duration = Duration()

    state = None
    error_type = None
    error_message = None

    df_compare_gap = None

    def __init__(self, configuration, source, expected):
        self.source = CaseItem(configuration["source"], source.connector, source.connection)
        self.expected = CaseItem(configuration["expected"], expected.connector, expected.connection)

    def load_data(self, obj_type:str):
        """ Load data from connector"""

        if obj_type == "source":
            obj = self.source
        else:
            obj = self.expected

        obj.duration.start = datetime.now()
        obj.df_data = obj.connector.get_data(obj.configuration, obj.connection)
        obj.duration.end = datetime.now()

    def load_data_error(self, obj_type:str, message:str):
        """Setup error message for data loading"""

        if obj_type == "source":
            obj = self.source
        else:
            obj = self.expected

        self.state = "error"
        self.error_type = "data"
        self.error_message = message
        obj.duration.end = datetime.now()

    def compare_dataframes(self):
        """Compare source and exptected dataframe"""

        self.compare_duration.start = datetime.now()

        count_source = len(self.source.df_data)
        count_expected = len(self.expected.df_data)

        if count_source != count_expected:
            self.error_type = "count"
            self.error_message = f"The count in source dataset ({count_source}) is differant than the count the in expected dataset ({count_expected})"

        if self.error_message is None and count_source != 0:
            #if compare_options is not None and compare_options["ignore"] is not None:
            #    df_source = df_source.drop(columns = compare_options["ignore"], axis = 1, errors = "ignore")
            #    df_expected = df_expected.drop(columns = compare_options["ignore"], axis = 1, errors = "ignore")

            df_columns_source = pd.DataFrame({ "columns": self.source.df_data.columns }).sort_values(by = ["columns"]).reset_index()
            df_columns_expected = pd.DataFrame({ "columns": self.expected.df_data.columns }).sort_values(by = ["columns"]).reset_index()

            message = "The headers are differant between source dataset and expected dataset"
            if len(df_columns_source) != len(df_columns_expected):
                self.error_message = message
                self.error_type = "headers"
            else:
                df_compare = df_columns_source.compare(df_columns_expected, result_names = ("source", "expected"))
                if len(df_compare) != 0 :
                    self.error_message = message
                    self.error_type = "headers"
                    self.df_compare_gap = df_compare

        if self.error_message is None and count_source != 0:
            #if compare_options is not None and compare_options["sort"] is not None:
            #    df_source = df_source.sort_values(by = compare_options["sort"]).reset_index()
            #    df_expected = df_expected.sort_values(by = compare_options["sort"]).reset_index()

            df_compare = self.source.df_data.compare(self.expected.df_data, result_names = ("source", "expected"))
            if len(df_compare) != 0 :
                self.error_message = "Some rows are not equals between source dataset and expected dataset"
                self.error_type = "data"
                self.df_compare_gap = df_compare

        self.compare_duration.end = datetime.now()

        if self.error_message is None:
            self.state = "passed"
        else:
            self.state = "failed"

    def compare_dataframes_error(self, message):
        """Setup error message for compare engine"""

        self.state = "Error"
        self.error_type = "compare"
        self.error_message = message
        self.compare_duration.end = datetime.now()

    def calculate_durations(self):
        """Calculate of durations"""

        self.source.duration.calculate_duration()
        self.expected.duration.calculate_duration()
        self.compare_duration.calculate_duration()

        self.global_duration.start = self.source.duration.start

        ends = []
        if self.source.duration.end is not None: ends.append(self.source.duration.end)
        if self.expected.duration.end is not None: ends.append(self.expected.duration.end)
        if self.compare_duration.end is not None: ends.append(self.compare_duration.end)

        self.global_duration.end = np.max(np.array(ends))
        self.global_duration.calculate_duration()

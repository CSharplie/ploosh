"""Module to manage test case"""
from dataclasses import dataclass
from datetime import datetime
import numpy as np
import pandas as pd

@dataclass
class StateStatistics:
    """Statistics of test case executions"""
    not_executed = 0
    executed = 0
    passed = 0
    failed = 0
    error = 0
    total = 0

    def add_state(self, state):
        """add new state to statistics"""
        if state == "passed": self.passed += 1
        if state == "failed": self.failed += 1
        if state == "error": self.error += 1
        if state == "notExecuted": self.not_executed += 1

        if state != "notExecuted": self.executed += 1

        self.total += 1


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
            duration = self.end - self.start
            self.duration = duration.seconds + (duration.microseconds / 1000000)


class CaseItem:
    """Structure of case item (source or expected)"""

    connector = None
    connection = None
    configuration = None

    duration = None
    df_data = None

    def __init__(self, configuration, connector, connection):
        self.duration = Duration()
        self.connector = connector
        self.connection = connection
        self.configuration = configuration

class Case:
    """Test case item"""

    options = None

    source = None
    expected = None

    global_duration = None
    compare_duration = None

    state = "notExecuted"
    error_type = None
    error_message = None

    df_compare_gap = None

    disabled = None

    def __init__(self, configuration, source, expected, options, disabled):
        self.source = CaseItem(configuration["source"], source.connector, source.connection)
        self.expected = CaseItem(configuration["expected"], expected.connector, expected.connection)
        self.options = options
        self.disabled = disabled
        self.global_duration = Duration()
        self.compare_duration = Duration()

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
            self.error_message = f"The count in source dataset ({count_source}) is differant than the count in the expected dataset ({count_expected})"

        if self.error_message is None and count_source != 0:
            if self.options is not None and self.options["ignore"] is not None:
                self.source.df_data = self.source.df_data.drop(columns = self.options["ignore"], axis = 1, errors = "ignore")
                self.expected.df_data = self.expected.df_data.drop(columns = self.options["ignore"], axis = 1, errors = "ignore")

            self.source.df_data.columns = map(str.lower, self.source.df_data.columns)
            self.expected.df_data.columns = map(str.lower, self.expected.df_data.columns)

            df_columns_source = pd.DataFrame({ "columns": self.source.df_data.columns }).sort_values(by = ["columns"]).reset_index(drop=True)
            df_columns_expected = pd.DataFrame({ "columns": self.expected.df_data.columns }).sort_values(by = ["columns"]).reset_index(drop=True)

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
            if self.options is not None and self.options["sort"] is not None:
                self.source.df_data = self.source.df_data.sort_values(by = self.options["sort"]).reset_index(drop=True)
                self.expected.df_data = self.expected.df_data.sort_values(by = self.options["sort"]).reset_index(drop=True)

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

    def compare_dataframes_with_spark(self, spark_session):
        """Compare source and expected dataframe using Spark"""

        self.compare_duration.start = datetime.now()

        count_source = self.source.df_data.count()
        count_expected = self.expected.df_data.count()

        if count_source != count_expected:
            self.error_type = "count"
            self.error_message = f"The count in source dataset ({count_source}) is different than the count in the expected dataset ({count_expected})"

        if self.error_message is None and count_source != 0:
            if self.options is not None and self.options["ignore"] is not None:
                ignore_columns = self.options["ignore"]
                self.source.df_data = self.source.df_data.drop(*ignore_columns)
                self.expected.df_data = self.expected.df_data.drop(*ignore_columns)

            source_columns = sorted(self.source.df_data.columns)
            expected_columns = sorted(self.expected.df_data.columns)

            if source_columns != expected_columns:
                self.error_message = "The headers are different between source dataset and expected dataset"
                self.error_type = "headers"

            if self.error_message is None and count_source != 0:
                #if self.options is not None and self.options["sort"] is not None:
                #    self.source.df_data = self.source.df_data.orderBy(*self.options["sort"]).drop("index")
                #    self.expected.df_data = self.expected.df_data.orderBy(*self.options["sort"]).drop("index")

                df_compare = self.source.df_data.exceptAll(self.expected.df_data)
                if df_compare.count() != 0:
                    self.error_message = "Some rows are not equal between source dataset and expected dataset"
                    self.error_type = "data"
                    self.df_compare_gap = df_compare.toPandas()

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

        ends = []
        if self.source.duration.end is not None: ends.append(self.source.duration.end)
        if self.expected.duration.end is not None: ends.append(self.expected.duration.end)
        if self.compare_duration.end is not None: ends.append(self.compare_duration.end)

        if len(ends) == 0:
            self.global_duration.duration = 0
        else:
            self.global_duration.start = self.source.duration.start
            self.global_duration.end = np.max(np.array(ends))
        self.global_duration.calculate_duration()

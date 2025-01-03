"""Module to manage test case"""
from dataclasses import dataclass
from datetime import datetime
import numpy as np
from engines.compare_engine_native import CompareEngineNative
from engines.compare_engine_spark import CompareEngineSpark
from engines.load_engine_native import LoadEngineNative
from engines.load_engine_spark import LoadEngineSpark

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
        """Add new state to statistics"""
        if state == "passed":
            self.passed += 1
        if state == "failed":
            self.failed += 1
        if state == "error":
            self.error += 1
        if state == "notExecuted":
            self.not_executed += 1

        if state != "notExecuted":
            self.executed += 1

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


@dataclass
class CaseItem:
    """Structure of case item (source or expected)"""
    connector = None
    connection = None
    configuration = None
    duration = None
    df_data = None
    count = 0

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
    success_rate = 1

    def __init__(self, configuration, source, expected, options, disabled):
        self.source = CaseItem(configuration["source"], source.connector, source.connection)
        self.expected = CaseItem(configuration["expected"], expected.connector, expected.connection)
        self.options = options
        self.disabled = disabled
        self.global_duration = Duration()
        self.compare_duration = Duration()

    def get_insensitive_item(self, name: str, items: list) -> str:
        """Get item from list case-insensitively"""
        for item in items:
            if name.upper().strip() == item.upper().strip():
                return item
        return name

    def load_data(self, obj_type: str):
        """Load data from connector"""
        if obj_type == "source":
            obj = self.source
        else:
            obj = self.expected

        obj.duration.start = datetime.now()

        if not self.source.connector.is_spark:
            load_engine = LoadEngineNative(obj.configuration, self.options, obj.connection)
        else:
            load_engine = LoadEngineSpark(obj.configuration, self.options, obj.connection)

        # Load data from connector
        obj.df_data = obj.connector.get_data(obj.configuration, obj.connection)

        # Execute load engine
        obj.df_data = load_engine.execute(obj.df_data)
        obj.count = load_engine.count

        obj.duration.end = datetime.now()

    def load_data_error(self, obj_type: str, message: str):
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
        """Compare source and expected dataframe"""
        self.compare_duration.start = datetime.now()

        compare_engine = CompareEngineNative(self.source.df_data, self.expected.df_data, self.options)
        compare_state = compare_engine.compare()

        self.error_message = compare_engine.error_message
        self.error_type = compare_engine.error_type
        self.df_compare_gap = compare_engine.df_compare_gap
        self.success_rate = compare_engine.success_rate

        self.compare_duration.end = datetime.now()

        if compare_state:
            self.state = "passed"
        else:
            self.state = "failed"

    def compare_dataframes_with_spark(self, spark_session):
        """Compare source and expected dataframe using Spark"""
        self.compare_duration.start = datetime.now()

        compare_engine = CompareEngineSpark(self.source.df_data, self.expected.df_data, self.options)
        compare_state = compare_engine.compare()

        self.error_message = compare_engine.error_message
        self.error_type = compare_engine.error_type
        self.df_compare_gap = compare_engine.df_compare_gap
        self.success_rate = compare_engine.success_rate

        self.compare_duration.end = datetime.now()

        if compare_state:
            self.state = "passed"
        else:
            self.state = "failed"
            self.state = "failed"

    def compare_dataframes_error(self, message):
        """Setup error message for compare engine"""
        self.state = "Error"
        self.error_type = "compare"
        self.error_message = message
        self.compare_duration.end = datetime.now()

    def calculate_durations(self):
        """Calculate durations"""
        self.source.duration.calculate_duration()
        self.expected.duration.calculate_duration()
        self.compare_duration.calculate_duration()

        ends = []
        if self.source.duration.end is not None:
            ends.append(self.source.duration.end)
        if self.expected.duration.end is not None:
            ends.append(self.expected.duration.end)
        if self.compare_duration.end is not None:
            ends.append(self.compare_duration.end)

        if len(ends) == 0:
            self.global_duration.duration = 0
        else:
            self.global_duration.start = self.source.duration.start
            self.global_duration.end = np.max(np.array(ends))
        self.global_duration.calculate_duration()

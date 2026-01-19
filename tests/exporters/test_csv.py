import csv
import os
import tempfile
import pytest
from datetime import datetime
from ploosh.exporters.exporter_csv import ExporterCSV


class MockDuration:
    def __init__(self, start, end, duration):
        self.start = start
        self.end = end
        self.duration = duration


class MockSource:
    def __init__(self, executed_action=None, count=10):
        self.duration = MockDuration(datetime(2024, 10, 7, 11, 55, 0), datetime(2024, 10, 7, 11, 55, 5), 5)
        self.count = count
        self.executed_action = executed_action


class MockCase:
    def __init__(self, state, source_executed_action=None, expected_executed_action=None, error_type=None, error_message=None):
        self.state = state
        self.source = MockSource(source_executed_action)
        self.expected = MockSource(expected_executed_action)
        self.compare_duration = MockDuration(datetime(2024, 10, 7, 11, 55, 13), datetime(2024, 10, 7, 11, 55, 15), 2)
        self.success_rate = 0.95
        self.error_type = error_type
        self.error_message = error_message
        self.df_compare_gap = None


@pytest.fixture
def exporter():
    exporter = ExporterCSV()
    with tempfile.TemporaryDirectory() as temp_dir:
        exporter.output_path = temp_dir
        yield exporter


def test_export_with_executed_action(exporter):
    cases = {
        "test_case_1": MockCase("passed", "SELECT * FROM table1", "SELECT * FROM table2"),
        "test_case_2": MockCase("failed", "/path/to/file.csv", "/path/to/file.json", "ValueError", "Some error message"),
        "test_case_3": MockCase("error", "SELECT *\nFROM table\nWHERE id = 1", "SELECT *\nFROM table2\nWHERE id = 1", "SyntaxError", "Invalid syntax")
    }

    exporter.export(cases)

    output_file = f"{exporter.output_path}/csv/test_results.csv"
    assert os.path.exists(output_file)

    with open(output_file, "r", encoding="UTF-8") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) == 4  # Header + 3 data rows

    # Check header
    header = rows[0]
    expected_header = [
        "name", "state",
        "source_start", "source_end", "source_duration", "source_count", "source_executed_action",
        "expected_start", "expected_end", "expected_duration", "expected_count", "expected_executed_action",
        "compare_start", "compare_end", "compare_duration", "success_rate",
        "error_type", "error_message"
    ]
    assert header == expected_header

    # Find column indices
    name_idx = header.index("name")
    state_idx = header.index("state")
    source_start_idx = header.index("source_start")
    source_end_idx = header.index("source_end")
    source_duration_idx = header.index("source_duration")
    source_count_idx = header.index("source_count")
    source_exec_idx = header.index("source_executed_action")
    expected_start_idx = header.index("expected_start")
    expected_end_idx = header.index("expected_end")
    expected_duration_idx = header.index("expected_duration")
    expected_count_idx = header.index("expected_count")
    expected_exec_idx = header.index("expected_executed_action")
    compare_start_idx = header.index("compare_start")
    compare_end_idx = header.index("compare_end")
    compare_duration_idx = header.index("compare_duration")
    success_rate_idx = header.index("success_rate")
    error_type_idx = header.index("error_type")
    error_message_idx = header.index("error_message")

    # Check first case (passed)
    row1 = rows[1]
    assert row1[name_idx] == "test_case_1"
    assert row1[state_idx] == "passed"
    assert row1[source_start_idx] == "2024-10-07T11:55:00Z"
    assert row1[source_end_idx] == "2024-10-07T11:55:05Z"
    assert row1[source_duration_idx] == "5"
    assert row1[source_count_idx] == "10"
    assert row1[source_exec_idx] == "SELECT * FROM table1"
    assert row1[expected_start_idx] == "2024-10-07T11:55:00Z"
    assert row1[expected_end_idx] == "2024-10-07T11:55:05Z"
    assert row1[expected_duration_idx] == "5"
    assert row1[expected_count_idx] == "10"
    assert row1[expected_exec_idx] == "SELECT * FROM table2"
    assert row1[compare_start_idx] == "2024-10-07T11:55:13Z"
    assert row1[compare_end_idx] == "2024-10-07T11:55:15Z"
    assert row1[compare_duration_idx] == "2"
    assert row1[success_rate_idx] == "0.95"
    assert row1[error_type_idx] == ""
    assert row1[error_message_idx] == ""

    # Check second case (failed)
    row2 = rows[2]
    assert row2[name_idx] == "test_case_2"
    assert row2[state_idx] == "failed"
    assert row2[source_exec_idx] == "/path/to/file.csv"
    assert row2[expected_exec_idx] == "/path/to/file.json"
    assert row2[error_type_idx] == "ValueError"
    assert row2[error_message_idx] == "Some error message"

    # Check third case (error with line returns)
    row3 = rows[3]
    assert row3[name_idx] == "test_case_3"
    assert row3[state_idx] == "error"
    assert row3[source_exec_idx] == "SELECT *\nFROM table\nWHERE id = 1"
    assert row3[expected_exec_idx] == "SELECT *\nFROM table2\nWHERE id = 1"
    assert row3[error_type_idx] == "SyntaxError"
    assert row3[error_message_idx] == "Invalid syntax"
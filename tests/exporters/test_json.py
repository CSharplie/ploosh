import json
import os
import tempfile
import pytest
from datetime import datetime
import pandas as pd
from ploosh.exporters.exporter_json import ExporterJSON


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
    def __init__(self, state, source_executed_action=None, expected_executed_action=None, error_type=None, error_message=None, df_compare_gap=None):
        self.state = state
        self.source = MockSource(source_executed_action)
        self.expected = MockSource(expected_executed_action)
        self.compare_duration = MockDuration(datetime(2024, 10, 7, 11, 55, 13), datetime(2024, 10, 7, 11, 55, 15), 2)
        self.success_rate = 0.95
        self.error_type = error_type
        self.error_message = error_message
        self.df_compare_gap = df_compare_gap


@pytest.fixture
def exporter():
    exporter = ExporterJSON()
    with tempfile.TemporaryDirectory() as temp_dir:
        exporter.output_path = temp_dir
        yield exporter


def test_export(exporter):
    cases = {
        "test_case_1": MockCase("passed", "SELECT * FROM table1", "SELECT * FROM table2"),
        "test_case_2": MockCase("failed", "/path/to/file.csv", "/path/to/file.json", "ValueError", "Some error message"),
        "test_case_3": MockCase("error", "SELECT *\nFROM table\nWHERE id = 1", "SELECT *\nFROM table2\nWHERE id = 1", "SyntaxError", "Invalid syntax")
    }

    execution_id = "test_execution_123"
    exporter.export(cases, execution_id)

    output_file = f"{exporter.output_path}/json/test_results.json"
    print(output_file)
    assert os.path.exists(output_file)

    with open(output_file, "r", encoding="UTF-8") as f:
        data = json.load(f)

    assert len(data) == 3

    # Check first case (passed)
    case1 = data[0]
    assert case1["execution_id"] == "test_execution_123"
    assert case1["name"] == "test_case_1"
    assert case1["state"] == "passed"
    assert "source" in case1
    assert case1["source"]["start"] == "2024-10-07T11:55:00Z"
    assert case1["source"]["end"] == "2024-10-07T11:55:05Z"
    assert case1["source"]["duration"] == 5
    assert case1["source"]["count"] == 10
    assert case1["source"]["executed_action"] == "SELECT * FROM table1"
    assert "expected" in case1
    assert case1["expected"]["start"] == "2024-10-07T11:55:00Z"
    assert case1["expected"]["end"] == "2024-10-07T11:55:05Z"
    assert case1["expected"]["duration"] == 5
    assert case1["expected"]["count"] == 10
    assert case1["expected"]["executed_action"] == "SELECT * FROM table2"
    assert "compare" in case1
    assert case1["compare"]["start"] == "2024-10-07T11:55:13Z"
    assert case1["compare"]["end"] == "2024-10-07T11:55:15Z"
    assert case1["compare"]["duration"] == 2
    assert case1["compare"]["success_rate"] == 0.95
    assert "error" not in case1

    # Check second case (failed)
    case2 = data[1]
    assert case2["execution_id"] == "test_execution_123"
    assert case2["name"] == "test_case_2"
    assert case2["state"] == "failed"
    assert case2["source"]["executed_action"] == "/path/to/file.csv"
    assert case2["expected"]["executed_action"] == "/path/to/file.json"
    assert "error" in case2
    assert case2["error"]["type"] == "ValueError"
    assert case2["error"]["message"] == "Some error message"

    # Check third case (error with line returns)
    case3 = data[2]
    assert case3["execution_id"] == "test_execution_123"
    assert case3["name"] == "test_case_3"
    assert case3["state"] == "error"
    assert case3["source"]["executed_action"] == "SELECT *\nFROM table\nWHERE id = 1"
    assert case3["expected"]["executed_action"] == "SELECT *\nFROM table2\nWHERE id = 1"
    assert case3["error"]["type"] == "SyntaxError"
    assert case3["error"]["message"] == "Invalid syntax"


def test_export_with_detail_file_path(exporter):
    # Create a mock DataFrame for comparison gap
    df_gap = pd.DataFrame({
        "column1": [1, 2, 3],
        "column2": ["a", "b", "c"]
    })
    
    cases = {
        "test_case_with_gap": MockCase(
            "failed", 
            "SELECT * FROM table1", 
            "SELECT * FROM table2", 
            "ComparisonError", 
            "Data mismatch found",
            df_compare_gap=df_gap
        ),
    }

    execution_id = "test_execution_456"
    exporter.export(cases, execution_id)

    output_file = f"{exporter.output_path}/json/test_results.json"
    assert os.path.exists(output_file)

    with open(output_file, "r", encoding="UTF-8") as f:
        data = json.load(f)

    assert len(data) == 1

    # Check that the detail_file_path is present
    case = data[0]
    assert case["name"] == "test_case_with_gap"
    assert case["state"] == "failed"
    assert "error" in case
    assert "detail_file_path" in case["error"]
    
    # Verify the detail file path format
    expected_path = f"{exporter.output_path}/json/test_results/test_case_with_gap.xlsx"
    assert case["error"]["detail_file_path"] == expected_path
    
    # Verify the Excel file was actually created
    assert os.path.exists(expected_path)
import pytest
from datetime import datetime
from ploosh.exporters.exporter_postgresql import ExporterPostgreSQL



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
    def __init__(self, state, source_executed_action=None, expected_executed_action=None, success_rate=0.95):
        self.state = state
        self.source = MockSource(source_executed_action)
        self.expected = MockSource(expected_executed_action)
        self.compare_duration = MockDuration(datetime(2024, 10, 7, 11, 55, 13), datetime(2024, 10, 7, 11, 55, 15), 2)
        self.success_rate = success_rate


class MockConnector:
    """Capture every execute_query call without touching a real database."""

    def __init__(self):
        self.calls = []  # list of dicts: {"query", "connection", "parameters"}

    def execute_query(self, query, connection, parameters=None):
        self.calls.append({
            "query": query,
            "connection": connection,
            "parameters": parameters,
        })
        return None


@pytest.fixture
def connection():
    return {"type": "postgresql", "hostname": "localhost", "database": "test_db", "port": 5432}


@pytest.fixture
def exporter(connection):
    exporter = ExporterPostgreSQL()
    exporter.connector = MockConnector()
    exporter.connection = connection
    return exporter


def test_create_table_called_once(exporter):
    cases = {
        "test_case_1": MockCase("passed", "SELECT * FROM table1", "SELECT * FROM table2"),
    }

    exporter.export(cases, "test_execution_123")

    # First call must be the CREATE TABLE statement, without parameters
    first_call = exporter.connector.calls[0]
    assert first_call["query"] == ExporterPostgreSQL.CREATE_TABLE_QUERY
    assert first_call["parameters"] is None


def test_insert_per_case(exporter):
    cases = {
        "test_case_1": MockCase("passed"),
        "test_case_2": MockCase("failed"),
        "test_case_3": MockCase("error"),
    }

    exporter.export(cases, "test_execution_123")

    # 1 CREATE TABLE + 1 INSERT per case
    assert len(exporter.connector.calls) == 1 + len(cases)

    insert_calls = exporter.connector.calls[1:]
    assert all(call["query"] == ExporterPostgreSQL.INSERT_QUERY for call in insert_calls)


def test_insert_parameters_mapping(exporter):
    cases = {
        "test_case_1": MockCase("passed", "SELECT * FROM table1", "SELECT * FROM table2"),
    }

    exporter.export(cases, "test_execution_123")

    params = exporter.connector.calls[1]["parameters"]

    assert params["execution_id"] == "test_execution_123"
    assert params["name"] == "test_case_1"
    assert params["state"] == "passed"
    assert params["source_duration"] == 5
    assert params["source_count"] == 10
    assert params["source_executed_action"] == "SELECT * FROM table1"
    assert params["expected_duration"] == 5
    assert params["expected_count"] == 10
    assert params["expected_executed_action"] == "SELECT * FROM table2"
    assert params["compare_duration"] == 2
    assert params["success_rate"] == 0.95


def test_execution_id_propagated(exporter):
    cases = {
        "test_case_1": MockCase("passed"),
        "test_case_2": MockCase("failed"),
    }

    exporter.export(cases, "shared_execution_id")

    insert_calls = exporter.connector.calls[1:]
    assert all(call["parameters"]["execution_id"] == "shared_execution_id" for call in insert_calls)


def test_datetime_passed_raw(exporter):
    cases = {
        "test_case_1": MockCase("passed"),
    }

    exporter.export(cases, "test_execution_123")

    params = exporter.connector.calls[1]["parameters"]

    # PostgreSQL exporter forwards raw datetime objects (no ISO string conversion)
    assert isinstance(params["source_start"], datetime)
    assert isinstance(params["source_end"], datetime)
    assert isinstance(params["expected_start"], datetime)
    assert isinstance(params["expected_end"], datetime)
    assert isinstance(params["compare_start"], datetime)
    assert isinstance(params["compare_end"], datetime)
    assert params["source_start"] == datetime(2024, 10, 7, 11, 55, 0)
    assert params["compare_end"] == datetime(2024, 10, 7, 11, 55, 15)


def test_connection_forwarded(exporter, connection):
    cases = {
        "test_case_1": MockCase("passed"),
    }

    exporter.export(cases, "test_execution_123")

    assert all(call["connection"] == connection for call in exporter.connector.calls)


def test_multiple_states(exporter):
    cases = {
        "passed_case": MockCase("passed"),
        "failed_case": MockCase("failed"),
        "error_case": MockCase("error"),
    }

    exporter.export(cases, "test_execution_123")

    states = [call["parameters"]["state"] for call in exporter.connector.calls[1:]]
    names = [call["parameters"]["name"] for call in exporter.connector.calls[1:]]

    assert states == ["passed", "failed", "error"]
    assert names == ["passed_case", "failed_case", "error_case"]


def test_empty_cases(exporter):
    exporter.export({}, "test_execution_123")

    # Only the CREATE TABLE statement should be executed, no INSERT
    assert len(exporter.connector.calls) == 1
    assert exporter.connector.calls[0]["query"] == ExporterPostgreSQL.CREATE_TABLE_QUERY


def test_query_uses_named_params(exporter):
    cases = {
        "test_case_1": MockCase("passed"),
    }

    exporter.export(cases, "test_execution_123")

    insert_query = exporter.connector.calls[1]["query"]

    for placeholder in [":execution_id", ":name", ":state", ":source_start", ":success_rate"]:
        assert placeholder in insert_query


def test_connection_missing_raises_error():
    exporter = ExporterPostgreSQL()
    exporter.connector = MockConnector()
    exporter.connection = None

    cases = {"test_case_1": MockCase("passed")}

    with pytest.raises(Exception, match="PostgreSQL export connection not found"):
        exporter.export(cases, "test_execution_123")


def test_connector_missing_raises_error():
    exporter = ExporterPostgreSQL()
    exporter.connector = None
    exporter.connection = {"type": "postgresql", "hostname": "localhost"}

    cases = {"test_case_1": MockCase("passed")}

    with pytest.raises(Exception, match="PostgreSQL connector not found"):
        exporter.export(cases, "test_execution_123")

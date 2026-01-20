import os
import pytest
from pyjeb import control_and_setup
from ploosh.connectors.connector_databricks import ConnectorDatabricks

@pytest.fixture
def connector():
    return ConnectorDatabricks()

def test_connection_with_token(connector):
    # Skip if no credentials
    if not os.environ.get("TEST_DATABRICKS_TOKEN") or not os.environ.get("TEST_DATABRICKS_HOSTNAME") or not os.environ.get("TEST_DATABRICKS_HTTP_PATH"):
        pytest.skip("Databricks credentials not available")

    configuration = {
        "query": "SELECT 1 as test_column",
        "connection": "debug"
    }

    connection = {
        "token": os.environ.get("TEST_DATABRICKS_TOKEN"),
        "hostname": os.environ.get("TEST_DATABRICKS_HOSTNAME"),
        "database": os.environ.get("TEST_DATABRICKS_DATABASE", "default"),
        "http_path": os.environ.get("TEST_DATABRICKS_HTTP_PATH"),
        "port": int(os.environ.get("TEST_DATABRICKS_PORT", "443"))
    }

    configuration = control_and_setup(configuration, connector.configuration_definition)
    connection = control_and_setup(connection, connector.connection_definition)

    df_test = connector.get_data(configuration, connection)

    assert len(df_test) >= 0  # At least runs without error
    assert connector.executed_action == "SELECT 1 as test_column"
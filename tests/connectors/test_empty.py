import pandas as pd
import pytest
from pyjeb import control_and_setup
from ploosh.connectors.connector_empty import ConnectorEmpty

@pytest.fixture
def connector():
    return ConnectorEmpty()

def test_get_data(connector):
    configuration = {}
    connection = {}

    configuration = control_and_setup(configuration, connector.configuration_definition)
    connection = control_and_setup(connection, connector.connection_definition)

    df = connector.get_data(configuration, connection)

    assert df.empty
    assert connector.executed_action == "empty"
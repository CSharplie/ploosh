import os
import pandas as pd
import pytest
from pyjeb import control_and_setup
from ploosh.connectors.connector_csv import ConnectorCSV

@pytest.fixture
def connector():
    return ConnectorCSV()

@pytest.fixture
def df_sales():
    return pd.read_csv("./tests/.data/sales.csv", delimiter=",")

def test_connection_with_tabulation(connector, df_sales):
    configuration = {
       "path": "./tests/.env/csv/sales_with_tab.csv",
       "delimiter": "\t"
    }

    configuration = control_and_setup(configuration, connector.configuration_definition)

    df_test = connector.get_data(configuration, None)

    assert len(df_test.compare(df_sales)) == 0

def test_connection_with_default(connector, df_sales):
    configuration = {
       "path": "./tests/.env/csv/sales_with_comma.csv"
    }

    configuration = control_and_setup(configuration, connector.configuration_definition)

    df_test = connector.get_data(configuration, None)

    assert len(df_test.compare(df_sales)) == 0
import os
import pandas as pd
import pytest
from pyjeb import control_and_setup
from ploosh.connectors.connector_json import ConnectorJSON

@pytest.fixture
def connector():
    return ConnectorJSON()

@pytest.fixture
def df_sales():
    return pd.read_csv(f"{os.getcwd()}/tests/.data/sales.csv", delimiter=",")


@pytest.fixture
def df_sales_with_two_rows():
    df = pd.read_csv(f"{os.getcwd()}/tests/.data/sales.csv", delimiter=",")
    df_first_2_rows = df.head(2)
    return df_first_2_rows


def test_json_default(connector, df_sales):
    configuration = {
       "path": f"{os.getcwd()}/tests/.env/json/sales.json"
    }

    configuration = control_and_setup(configuration, connector.configuration_definition)

    df_test = connector.get_data(configuration, None)

    assert len(df_test.compare(df_sales)) == 0
    assert connector.executed_action == f"{os.getcwd()}/tests/.env/json/sales.json"


def test_json_with_lines_true(connector, df_sales):
    configuration = {
       "path": f"{os.getcwd()}/tests/.env/json/sales_lines_true.json",
       "lines": True
    }

    configuration = control_and_setup(configuration, connector.configuration_definition)

    df_test = connector.get_data(configuration, None)

    assert len(df_test.compare(df_sales)) == 0
    assert connector.executed_action == f"{os.getcwd()}/tests/.env/json/sales_lines_true.json"


def test_json_with_two_rows(connector, df_sales_with_two_rows):
    configuration = {
       "path": f"{os.getcwd()}/tests/.env/json/sales_lines_true.json",
       "lines": True,
       "nrows": 2
    }

    configuration = control_and_setup(configuration, connector.configuration_definition)

    df_test = connector.get_data(configuration, None)

    assert len(df_test.compare(df_sales_with_two_rows)) == 0
    assert connector.executed_action == f"{os.getcwd()}/tests/.env/json/sales_lines_true.json"


def test_json_with_specific_encoding(connector, df_sales):
    configuration = {
       "path": f"{os.getcwd()}/tests/.env/json/sales-ISO-8859-1.json"
    }

    configuration = control_and_setup(configuration, connector.configuration_definition)

    df_test = connector.get_data(configuration, None)

    assert len(df_test.compare(df_sales)) == 0
    assert connector.executed_action == f"{os.getcwd()}/tests/.env/json/sales-ISO-8859-1.json"

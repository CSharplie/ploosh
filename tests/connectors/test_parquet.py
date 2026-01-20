import os
import pandas as pd
import pytest
from pyjeb import control_and_setup
from ploosh.connectors.connector_parquet import ConnectorParquet

@pytest.fixture
def connector():
    return ConnectorParquet()


@pytest.fixture
def df_sales():
    return pd.read_csv(f"{os.getcwd()}/tests/.data/sales.csv", delimiter=",")

@pytest.fixture
def df_sales_with_specific_columns():
    df = pd.read_csv(f"{os.getcwd()}/tests/.data/sales.csv", delimiter=",")
    df_selected_columns = df[["sale_id", "seller_name", "card_name", "quantity"]]
    return df_selected_columns

@pytest.fixture
def df_sales_with_filters():
    df = pd.read_csv(f"{os.getcwd()}/tests/.data/sales.csv", delimiter=",")
    df_filtered = df[(df["sale_id"] > 10) & (df['quantity'] == 1)]
    df_filtered = df_filtered.reset_index(drop=True)
    return df_filtered


def test_default(connector, df_sales):
    configuration = {
       "path": "./tests/.env/parquet/sales.parquet",
    }

    configuration =  control_and_setup(configuration, connector.configuration_definition)
    df_test = connector.get_data(configuration, {})

    assert len(df_test.compare(df_sales)) == 0
    assert connector.executed_action == "./tests/.env/parquet/sales.parquet"


def test_with_specific_columns(connector, df_sales_with_specific_columns):
    configuration = {
       "path": "./tests/.env/parquet/sales.parquet",
       "columns" : ["sale_id", "seller_name", "card_name", "quantity"]
    }

    configuration =  control_and_setup(configuration, connector.configuration_definition)
    df_test = connector.get_data(configuration, {})

    assert len(df_test.compare(df_sales_with_specific_columns)) == 0
    assert connector.executed_action == "./tests/.env/parquet/sales.parquet"


def test_with_filters(connector, df_sales_with_filters):
    configuration = {
       "path": "./tests/.env/parquet/sales.parquet",
       "filters" : [{"column": "sale_id", "operator": ">", "value": 10},
                    {"column": "quantity", "operator": "==", "value": 1}]
    }

    configuration =  control_and_setup(configuration, connector.configuration_definition)
    df_test = connector.get_data(configuration, {})

    assert len(df_test.compare(df_sales_with_filters)) == 0
    assert connector.executed_action == "./tests/.env/parquet/sales.parquet"

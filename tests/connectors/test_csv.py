import os
import pandas as pd
import pytest
from pyjeb import control_and_setup
import numpy as np
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

def test_connection_with_schema(connector, df_sales):
    # schecma : sale_id,seller_name,card_name,card_rarity,card_condition,price,quantity,sale_date,card_set,buyer_name,transaction_status
    configuration = {
       "path": "./tests/.env/csv/sales_with_schema.csv",
       "schema": {
              "sale_id": "string",
              "seller_name": "string",
              "card_name": "string",
              "card_rarity": "string",
              "card_condition": "string",
              "price": "float",
              "quantity": "int",
              "sale_date": "datetime",
              "card_set": "string",
              "buyer_name": "string",
              "transaction_status": "string"
         }
    }
    configuration = control_and_setup(configuration, connector.configuration_definition)
    df_test = connector.get_data(configuration, None)
    
    # check if the dtypes are as expected
    assert df_test.dtypes["sale_id"] == "string"
    assert df_test.dtypes["seller_name"] == "string"
    assert df_test.dtypes["card_name"] == "string"
    assert df_test.dtypes["card_rarity"] == "string"
    assert df_test.dtypes["card_condition"] == "string"
    assert df_test.dtypes["price"] == np.dtype("float64")
    assert df_test.dtypes["quantity"] == np.dtype("int64")
    assert df_test.dtypes["sale_date"] == np.dtype("datetime64[ns]")
    assert df_test.dtypes["card_set"] == "string"
    assert df_test.dtypes["buyer_name"] == "string"
    assert df_test.dtypes["transaction_status"] == "string"



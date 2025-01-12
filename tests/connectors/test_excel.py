import os
import pandas as pd
import pytest
from pyjeb import control_and_setup
from ploosh.connectors.connector_excel import ConnectorExcel

@pytest.fixture
def connector():
    return ConnectorExcel()

@pytest.fixture
def df_sales():
    return pd.read_csv("./tests/.data/sales.csv", delimiter=",", date_format = "%Y-%m-%d", parse_dates=["sale_date"])

def test_get_data(connector, df_sales):
    configuration = {
        "path": "./tests/.env/excel/sales.xlsx",
        "sheet_name": "sales"
    }
    
    configuration = control_and_setup(configuration, connector.configuration_definition)
    
    df_test = connector.get_data(configuration, None)
    
    assert len(df_test.compare(df_sales)) == 0
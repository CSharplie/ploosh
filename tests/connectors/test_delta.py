import os
import pandas as pd
import pytest
from pyjeb import control_and_setup
from ploosh.connectors.connector_delta import ConnectorDELTA


@pytest.fixture
def connector():
    return ConnectorDELTA()


@pytest.fixture
def df_sales():
    return pd.read_csv(f"{os.getcwd()}/tests/.data/sales.csv", delimiter=",")


def test_default(connector, df_sales):
    configuration = {
       "path": f"./tests/.env/delta/sales"
    }
    configuration = control_and_setup(configuration, connector.configuration_definition)
    df_test = connector.get_data(configuration, None)

    assert len(df_test.compare(df_sales)) == 0
import os
import pandas as pd
import pytest
import urllib
from pyjeb import control_and_setup
from ploosh.connectors.connector_mssql import ConnectorMSSQL

@pytest.fixture
def connector():
    return ConnectorMSSQL()

@pytest.fixture
def df_sales():
    return pd.read_csv("./tests/.data/sales.csv", delimiter=",", date_format = "%Y-%m-%d", parse_dates=["sale_date"])

def test_connection_with_password(connector, df_sales):
    configuration = {
        "query": "select * from sales;",
        "connection": "debug"
    }

    connection = {
        "hostname": "localhost",
        "username": "sa",
        "password": os.environ.get("TEST_DB_PASSWORD"),
        "database": "ploosh",
        "driver": "ODBC Driver 17 for SQL Server",
        "encrypt": False,
    }
    connection = control_and_setup(connection, connector.connection_definition)

    df_test = connector.get_data(configuration, connection)

    assert len(df_test.compare(df_sales)) == 0


def test_connection_with_connection_string(connector, df_sales):
    configuration = {
        "query": "select * from sales;",
        "connection": "debug"
    }

    password = urllib.parse.quote_plus(os.environ.get('TEST_DB_PASSWORD'))
    connection = {
        "mode": "connection_string",
        "connection_string": f"mssql+pyodbc://sa:{password}@localhost/ploosh?driver=ODBC+Driver+17+for+SQL+Server"
    }

    connection = control_and_setup(connection, connector.connection_definition)

    df_test = connector.get_data(configuration, connection)

    assert len(df_test.compare(df_sales)) == 0
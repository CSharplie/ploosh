import os
import pandas as pd
from pyjeb import control_and_setup
from ploosh.connectors.connector_postgresql import ConnectorPostgreSQL

connector = ConnectorPostgreSQL()

connection_password = {
    "hostname": "localhost",
    "username": "ploosh",
    "password": os.environ.get("TEST_DB_PASSWORD"),
    "database": "ploosh"
}

control_and_setup(connection_password, connector.connection_definition)

df_sales = pd.read_csv("./tests/.env/csv/sales.csv", delimiter=",")

def test_connection_with_password():
    configuration = {
        "query": "select * from sales;",
        "connection": "debug"
    }

    control_and_setup(configuration, connector.configuration_definition)

    df_test = connector.get_data(configuration, connection_password)

    

    assert df_test.compare(df_sales)

     

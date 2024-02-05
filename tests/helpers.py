import pandas as pd
import json
from pyjeb import control_and_setup

from ploosh.connectors.connector import Connector

def get_dataframe_from_query(query, connector:Connector):
    with open(f"./tests/connections/{connector.name.lower()}.json") as f:
        connection = control_and_setup(json.load(f), connector.connection_definition)

    configuration = { "query" : query }
    
    return connector.get_data(configuration, connection)


def get_users_dataset():
    return pd.read_csv("./tests/data/users.csv")

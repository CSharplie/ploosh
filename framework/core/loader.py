from datetime import datetime
from core.connectors import get_data_from_connector

def load_data_from_source(dataset_definition, connections):
    connection_name = dataset_definition["connection"]

    if connection_name not in connections.keys():
        raise f"02x001 - The connection '{connection_name}' do not exists"
    connection = connections[connection_name]

    start_time = datetime.now()
    df_data = get_data_from_connector(connection["type"], dataset_definition, connection)
    end_time = datetime.now()

    duration = (end_time - start_time).microseconds / 60000000

    return {
        "duration" : duration,
        "df_data" : df_data
    }

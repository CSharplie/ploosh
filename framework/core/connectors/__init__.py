from core.connectors.connector_mssql import get_data_from_mssql
from core.connectors.connector_csv import get_data_from_csv

def get_data_from_connector(name, dataset_definition, connection):
    match name:
        case "mssql":
            return get_data_from_mssql(dataset_definition, connection)
        case "csv":
            return get_data_from_csv(dataset_definition)
        case _:
            raise f"02x002 - The connection type '{name}' do not exists"

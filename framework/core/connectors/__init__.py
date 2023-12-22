import core.connectors.connector_csv as CSV
import core.connectors.connector_mssql as MSSQL

def get_data_from_connector(name, dataset_definition, connection):
    match name:
        case "mssql":
            return MSSQL.get_data(dataset_definition, connection)
        case "csv":
            return CSV.get_data(dataset_definition)
        case _:
            raise f"02x002 - The connection type '{name}' do not exists"

def get_connection_configuration(name):
    match name:
        case "mssql":
            return MSSQL.get_connection_configuration()
        case "csv":
            return CSV.get_connection_configuration()
        case _:
            raise f"02x002 - The connection type '{name}' do not exists"

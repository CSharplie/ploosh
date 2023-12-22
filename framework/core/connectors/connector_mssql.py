import pandas as pd
import urllib

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from core.miscellaneous import get_parameter_value

def get_data_from_mssql(test_case_definition, connection):
    query = get_parameter_value(test_case_definition, "query", "03x003")
    mode = get_parameter_value(connection, "mode", "03x003")

    match mode:
        case "connection_string":
            connection_string = get_parameter_value(connection, "connection_string", "03x003")
        case "password":
            hostname = get_parameter_value(connection, "hostname", "03x003")
            database = get_parameter_value(connection, "database", "03x003")
            user_name = get_parameter_value(connection, "username", "03x003")
            password = urllib.parse.quote_plus(get_parameter_value(connection, "password", "03x003"))
            driver = get_parameter_value(connection, "driver", "03x003", "SQL Server")

            connection_string = f"DRIVER={driver};SERVER={hostname};DATABASE={database};UID={user_name};PWD={password}"
        case _:
            raise f"01x001 - The mode '{mode}' do not exists"


    connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
    engine = create_engine(connection_url)
    df = pd.read_sql(query, engine)

    return df
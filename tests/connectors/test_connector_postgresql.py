from tests.helpers import get_users_dataset, get_dataframe_from_query
from ploosh.connectors.connector_postgresql import ConnectorPostgreSQL

def test_connection_with_password():
    query = "select id, first_name, last_name, email, gender, ip_address from users order by id;"

    df_connector = get_dataframe_from_query(query, ConnectorPostgreSQL())
    df_local = get_users_dataset()

    assert len(df_connector.compare(df_local)) == 0


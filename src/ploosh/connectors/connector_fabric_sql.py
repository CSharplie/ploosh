import struct
import pyodbc
import pandas as pd
from connectors.connector import Connector
from azure.identity import ClientSecretCredential, InteractiveBrowserCredential, UsernamePasswordCredential
from itertools import chain, repeat

class ConnectorFabricSQL(Connector):
    """Connector to read Analysis Services Model using ADOMD"""

    def __init__(self):
        
        self.name = "FABRIC_SQL"
        self.connection_definition = [
            {
                "name": "mode",
                "default" : "oauth",
                "validset": ["oauth"] #, "token", "credentials", "spn"]
            },
            {
                "name": "token",
                "default" : None
            },
            {
                "name": "username",
                "default": None
            },
            {
                "name": "password",
                "default": None
            }, 
            {
                "name": "tenant_id",
                "default" : None
            }, 
            {
                "name": "client_id",
                "default" : None
            }, 
            {
                "name": "client_secret",
                "default" : None
            },
            {
                "name": "scope",
                "default" : 'https://analysis.windows.net/powerbi/api/.default'
            },
            {
                "name": "server"
            }
        ]
        self.configuration_definition = [
            { 
                "name": "query"
            }
        ]

    def get_data(self, configuration: dict, connection: dict):
        """Get data from source"""

        mode = connection["mode"]
        server = connection["server"]
        query = configuration["query"] # SQL Query

        # Determine the connection mode and set up the connection string accordingly

        # If using OAuth for authentication, opens a login page in the browser
        if mode == "oauth":
            # Define the connection string for ODBC Driver 18 for SQL Server
            connection_string = f"Driver={{ODBC Driver 18 for SQL Server}};Server={server},1433;Encrypt=Yes;TrustServerCertificate=No"

            # Retrieve an access token using InteractiveBrowserCredential
            credential = InteractiveBrowserCredential()
            token_object = credential.get_token("https://database.windows.net//.default")  # Retrieve an access token valid to connect to SQL databases
            token_as_bytes = bytes(token_object.token, "UTF-8")  # Convert the token to a UTF-8 byte string
            encoded_bytes = bytes(chain.from_iterable(zip(token_as_bytes, repeat(0))))  # Encode the bytes to a Windows byte string
            token_bytes = struct.pack("<i", len(encoded_bytes)) + encoded_bytes  # Package the token into a bytes object
            attrs_before = {1256: token_bytes}

        # If using a provided token for authentication
        elif mode == "token":
            token = connection["token"]  # Retrieve the token from the connection definition
            # Define the connection string for ODBC Driver 18 for SQL Server using the provided token
            connection_string = f"Driver={{ODBC Driver 18 for SQL Server}};Server={server},1433;User Id=;Password={token};Encrypt=Yes;TrustServerCertificate=No"
        
        # If using a service principal name (SPN) for authentication
        elif mode == "spn":
            scope = connection["scope"]  # Retrieve the scope from the connection definition
            tenant_id = connection["tenant_id"]  # Retrieve the tenant ID from the connection definition
            client_id = connection["client_id"]  # Retrieve the client ID from the connection definition
            client_secret = connection["client_secret"]  # Retrieve the client secret from the connection definition
            authority = f'https://login.microsoftonline.com/'  # Define the authority URL
            # Retrieve an access token using ClientSecretCredential
            credential = ClientSecretCredential(tenant_id, client_id, client_secret)#, authority=authority)
            token = credential.get_token(scope)  # Retrieve the token
            token_string = token.token   # Extract the token string
            # Define the connection string for ODBC Driver 18 for SQL Server using the token string
            connection_string = f"Driver={{ODBC Driver 18 for SQL Server}};Server={server},1433;User Id=;Password={token_string};Encrypt=Yes;TrustServerCertificate=No"
        
        # If using username and password for authentication
        elif mode == "credentials":
            username = connection["username"]  # Retrieve the username from the connection definition
            password = connection["password"]  # Retrieve the password from the connection definition
            # Define the connection string for ODBC Driver 18 for SQL Server using the username and password
            connection_string = f"Driver={{ODBC Driver 18 for SQL Server}};Server={server},1433;User Id={username};Password={password};Encrypt=Yes;TrustServerCertificate=No"

        try:
            # Create and open connection to AS instance
            con = pyodbc.connect(connection_string, attrs_before=attrs_before)
        except Exception as conection_error:
            error_message = str(conection_error)
            raise Exception(f"Error connecting to source:\n{str(error_message)}")
        
        try:
            with con.cursor() as cur:
                cur.execute(query)  # Execute the query
                result = cur.fetchall()  # Fetch all results
                column_name=[i[0] for i in cur.description]  # Get column names from cursor description
                df = pd.DataFrame.from_records(result, columns = column_name)  # Create a DataFrame with column names
            
            # Proactively close connection
            cur.close()
            con.close()

            return df
        except Exception as query_error:
            # Ensure the cursor and connection are closed in case of an error
            cur.close()
            con.close()
            error_message = str(query_error)
            raise Exception(f"Error executing query:\n{str(error_message)}")
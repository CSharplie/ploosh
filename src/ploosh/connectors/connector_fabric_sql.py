import pandas as pd
from connectors.connector import Connector
from azure.identity import ClientSecretCredential, InteractiveBrowserCredential, UsernamePasswordCredential
from sys import path
from pathlib import Path
import pyodbc
import os

from itertools import chain, repeat
import struct

class ConnectorFabricSql(Connector):
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
                "name": "database_name"
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
        database_name = connection["database_name"] # For local .pbix --> Dataset ID: in DAX Studio, right click to model name and choose "copy Database ID"

        query = configuration["query"] # DAX Query


        # will open a login page in browser (if local AS instance, will connect automatically)
        if mode == "oauth":
            #connection_string = f'Provider=MSOLAP;Data Source={server};Catalog={dataset_id};'

            connection_string = f"Driver={{ODBC Driver 18 for SQL Server}};Server={server},1433;Database={database_name};Encrypt=Yes;TrustServerCertificate=No"

            credential = InteractiveBrowserCredential()
            token_object = credential.get_token("https://database.windows.net//.default") # Retrieve an access token valid to connect to SQL databases
            token_as_bytes = bytes(token_object.token, "UTF-8") # Convert the token to a UTF-8 byte string
            encoded_bytes = bytes(chain.from_iterable(zip(token_as_bytes, repeat(0)))) # Encode the bytes to a Windows byte string
            token_bytes = struct.pack("<i", len(encoded_bytes)) + encoded_bytes # Package the token into a bytes object
            attrs_before = {1256: token_bytes}

        # uses the token provided in the connection_definition
        elif mode == "token":
            token = connection["token"]
            connection_string = f'Provider=MSOLAP;Data Source={server};Catalog={database_name};User Id=;Password={token};Impersonation Level=Impersonate;'
        
        # get a token from a registered azure app
        elif mode == "spn":
            scope = connection["scope"]
            tenant_id = connection["tenant_id"]
            client_id = connection["client_id"]
            client_secret = connection["client_secret"]
            authority = f'https://login.microsoftonline.com/'
            credential = ClientSecretCredential(tenant_id, client_id, client_secret)#, authority=authority)
            token = credential.get_token(scope)
            token_string = token.token
            connection_string = f'Provider=MSOLAP;Data Source={server};Catalog={database_name};User Id=;Password={token_string};Impersonation Level=Impersonate;'
        
        # uses username and password
        elif mode == "credentials":
            username = connection["username"]
            password = connection["password"]
            connection_string = f'Provider=MSOLAP;Data Source={server};Catalog={database_name};User Id={username};Password={password};'


        # Create and open connection to AS instance
        con = pyodbc.connect(connection_string, attrs_before=attrs_before)

        # df = pd.read_sql(query, con)

        """
        try:
            con.open()  # Open the connection
        except:
            raise ValueError("Can't connect to the AS Instance")
        """

        # execute DAX query
        with con.cursor() as cur:
            try:
                cur.execute(query)
                result = cur.fetchall()
                dfTest = pd.DataFrame(result)
                column_name=[i[0] for i in cur.description]
                df = pd.DataFrame.from_records(result, columns = column_name)
                print(df)

                # Proactively close connection to AS instance
                # con.close()  

                return df
            except Exception as query_error:
                error_message = str(query_error)
                # Keep only error message without Technical Details
                error_summary = error_message.split("Technical Details")[0].strip().split("\r\n   at")[0].strip()
                raise Exception(f"Erreur lors de l'exécution de la requête :\n{str(error_summary)}")
import pandas as pd
from connectors.connector import Connector
from azure.identity import ClientSecretCredential, InteractiveBrowserCredential, UsernamePasswordCredential
from sys import path
from pathlib import Path
import os

class ConnectorAnalysisServices(Connector):
    """Connector to read Analysis Services Model using ADOMD"""

    def __init__(self):
        ## ADOMD.dll ##
            # Using dll file put into src\ploosh\connectors\modules
            # The file need to be packaged to work here
            # need to use the absPath (!!! check if it works on linux !!!)
        root = Path(r"\Program Files\Microsoft.NET\ADOMD.NET\\")
        adomd_path = str(max((root).iterdir()))
        path.append(adomd_path)
        #absPath = os.path.dirname(__file__)
        #path.append(absPath + '\\modules')

            # NEED to pip install pythonnet to make pyadomd work !!
        global Pyadomd
        from pyadomd import Pyadomd
        ## ADOMD.dll -- END ##

        self.name = "ANALYSISSERVICES"
        self.connection_definition = [
            {
                "name": "mode",
                "default" : "oauth",
                "validset": ["oauth", "token", "credentials", "spn"]
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
                "name": "dataset_id"
            },
            {
                "name": "hostname"
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
        
        hostname = connection["hostname"]
        dataset_id = connection["dataset_id"] # For local .pbix --> Dataset ID: in DAX Studio, right click to model name and choose "copy Database ID"

        query = configuration["query"] # DAX Query


        # will open a login page in browser (if local AS instance, will connect automatically)
        if mode == "oauth":
            connection_string = f'Provider=MSOLAP;Data Source={hostname};Catalog={dataset_id};'
        
        # uses the token provided in the connection_definition
        elif mode == "token":
            token = connection["token"]
            connection_string = f'Provider=MSOLAP;Data Source={hostname};Catalog={dataset_id};User Id=;Password={token};Impersonation Level=Impersonate;'
        
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
            connection_string = f'Provider=MSOLAP;Data Source={hostname};Catalog={dataset_id};User Id=;Password={token_string};Impersonation Level=Impersonate;'
        
        # uses username and password
        elif mode == "credentials":
            username = connection["username"]
            password = connection["password"]
            connection_string = f'Provider=MSOLAP;Data Source={hostname};Catalog={dataset_id};User Id={username};Password={password};'


        # Create and open connection to AS instance
        con = Pyadomd(connection_string)
        con.open()  # Open the connection

        # execute DAX query
        result = con.cursor().execute(query)

        # Load result into a Dataframe
        column_name=[i.name for i in result.description]
        df = pd.DataFrame(result.fetchone(), columns = column_name)

        # Proactively close connection to AS instance
        con.close()  

        return df
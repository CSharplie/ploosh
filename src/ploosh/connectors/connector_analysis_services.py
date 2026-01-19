"""Analysis Services connector."""

from pathlib import Path
from sys import path
import pandas as pd
from azure.identity import ClientSecretCredential
from connectors.connector import Connector

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

        self.name = "ANALYSIS_SERVICES"
        self.connection_definition = [
            {
                "name": "mode",
                "default": "oauth",
                "validset": ["oauth", "pbix"]  # , "token", "credentials", "spn"]
            },
            {
                "name": "token",
                "default": None
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
                "default": None
            },
            {
                "name": "client_id",
                "default": None
            },
            {
                "name": "client_secret",
                "default": None
            },
            {
                "name": "scope",
                "default": 'https://analysis.windows.net/powerbi/api/.default'
            },
            {
                "name": "dataset_id"
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
        dataset_id = connection["dataset_id"]  # For local .pbix --> Dataset ID: in DAX Studio, right click to model name and choose "copy Database ID"

        query = configuration["query"]  # DAX Query

        # will open a login page in browser (if local AS instance, will connect automatically)
        if mode == "oauth":
            connection_string = f'Provider=MSOLAP;Data Source={server};Catalog={dataset_id};'

        # will open a login page in browser (if local AS instance, will connect automatically)
        elif mode == "pbix":
            connection_string = f'Provider=MSOLAP;Data Source={server};Catalog={dataset_id};'

        # uses the token provided in the connection_definition
        elif mode == "token":
            token = connection["token"]
            connection_string = f'Provider=MSOLAP;Data Source={server};Catalog={dataset_id};User Id=;Password={token};Impersonation Level=Impersonate;'

        # get a token from a registered azure app
        elif mode == "spn":
            scope = connection["scope"]
            tenant_id = connection["tenant_id"]
            client_id = connection["client_id"]
            client_secret = connection["client_secret"]
            credential = ClientSecretCredential(tenant_id, client_id, client_secret)
            token = credential.get_token(scope)
            token_string = token.token
            connection_string = f'Provider=MSOLAP;Data Source={server};Catalog={dataset_id};User Id=;Password={token_string};Impersonation Level=Impersonate;'

        # uses username and password
        elif mode == "credentials":
            username = connection["username"]
            password = connection["password"]
            connection_string = f'Provider=MSOLAP;Data Source={server};Catalog={dataset_id};User Id={username};Password={password};'

        # Create and open connection to AS instance
        con = Pyadomd(connection_string)
        try:
            con.open()  # Open the connection
        except:
            raise ValueError("Can't connect to the AS Instance")

        # Store the executed query for reference
        self.executed_action = query

        # execute DAX query
        with con.cursor() as cur:
            try:
                cur.execute(query)
                result = cur.fetchone()
                column_name = [i.name for i in cur.description]
                df = pd.DataFrame(result, columns=column_name)

                # Proactively close connection to AS instance
                con.close()

                return df
            except Exception as query_error:
                error_message = str(query_error)
                # Keep only error message without Technical Details
                error_summary = error_message.split("Technical Details")[0].strip().split("\r\n   at")[0].strip()
                raise Exception(f"Erreur lors de l'exécution de la requête :\n{str(error_summary)}")

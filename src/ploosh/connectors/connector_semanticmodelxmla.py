# pylint: disable=R0903
"""Connector to read Semantic Model from Fabric XMLA endpoint"""

import pandas as pd
import requests
from azure.identity import ClientSecretCredential, InteractiveBrowserCredential, UsernamePasswordCredential
from connectors.connector import Connector
import json

class ConnectorSemanticModel(Connector):
    """Connector to read Semantic Model using Fabric XMLA endpoint"""

    def __init__(self):
        self.name = "SEMANTICMODEL"
        self.connection_definition = [
            {
                "name": "mode",
                "default" : "oauth",
                "validset": ["oauth", "token", "spn"]
            }, 
            {
                "name": "token",
                "default" : None
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
                "name": "dataset_id"
            }
        ]
        self.configuration_definition = [
            { 
                "name": "query" 
            }, 
            {
                "name": "body",
                "default": None
            }
        ]

    def get_data(self, configuration: dict, connection: dict):
        """Get data from source"""


        mode = connection["mode"]
        dataset_id = connection["dataset_id"]
        query = configuration["query"]


        if mode == "oauth":
            interactive_browser_credential_class = InteractiveBrowserCredential()
            scope = 'https://analysis.windows.net/powerbi/api/.default'
            access_token_class = interactive_browser_credential_class.get_token(scope)
            token_string = access_token_class.token

        # uses the token provided in the connection_definition
        elif mode == "token":
            token_string = connection["token"]

        # get a token from a registered azure app
        elif mode == "spn":
            scope = 'https://analysis.windows.net/powerbi/api/.default'
            tenant_id = connection["tenant_id"]
            client_id = connection["client_id"]
            client_secret = connection["client_secret"]
            authority = f'https://login.microsoftonline.com/'
            credential = ClientSecretCredential(tenant_id, client_id, client_secret, authority=authority)
            token = credential.get_token(scope)
            token_string = token.token #need to define header
        


        # Initialize query
        post_query = f'https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}/executeQueries'
        header = {'Authorization': f'Bearer {token_string}','Content-Type' : 'application/json'}
        body = '''{
        "queries": [
            {
            "query": "%s"
        }
        ],
        "serializerSettings": {
            "includeNulls": "true"
        }
        }''' % (query)


        post_r = requests.post(url=post_query,data=body, headers=header)

        if post_r.status_code == 400:
            response = json.loads(post_r.text)
            error_code = response['error']['code'] + "\n"
            error_message = response['error']['pbi.error']['details'][0]['detail']['value']
            raise ValueError("DAX Execution Error : " + error_code + "\n" + error_message)

        if post_r.status_code == 404:
            raise ValueError("Connection issue: PowerBIEntityNotFound")


        output = post_r.json()
        dfResults = pd.DataFrame(output)
        dfTables = pd.DataFrame(dfResults["results"][0])
        dfRows = pd.DataFrame(dfTables["tables"][0])
        flattenData = dfRows.values.flatten()
        df = pd.json_normalize(flattenData) # type: ignore

        return df
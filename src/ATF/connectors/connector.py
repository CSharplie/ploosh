# pylint: disable=R0903,W0613
"""Connector to acces to remote data"""

class Connector:
    """Connector to acces to remote data"""
    name = None
    connection_definition = None
    configuration_definition = None

    def get_data(self, configuration:dict, connection:dict):
        """Get data from connector"""
        return None

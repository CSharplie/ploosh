# pylint: disable=R0903,W0613
"""Connector to access to remote data"""

class Connector:
    """Connector to access to remote data"""
    name = None
    connection_definition = None
    configuration_definition = None
    is_spark = False
    spark = None

    def get_data(self, configuration:dict, connection:dict):
        """Get data from connector"""
        return None

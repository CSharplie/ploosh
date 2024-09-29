# pylint: disable=R0903,W0613
"""Connector to access to remote data"""


class Connector:
    """Connector to access to remote data"""
    name = None  # Name of the connector
    connection_definition = None  # Definition of the connection parameters
    configuration_definition = None  # Definition of the configuration parameters
    is_spark = False  # Flag to indicate if the connector uses Spark
    spark = None  # Spark session object

    def get_data(self, configuration: dict, connection: dict):
        """Get data from connector"""
        return None  # This method should be overridden by subclasses to fetch data

# pylint: disable=R0903,C0415,C0103
"""Connector to read Dremio data with Spark"""

from connectors.connector import Connector

class ConnectorDremioSpark(Connector):
    """Connector to read Fabric KQL data with Spark"""
    
    def __init__(self):
        # Initialize the connector with its name and configuration definitions
        self.name = "DREMIO_SPARK"
        self.is_spark = True  # Indicates that this connector uses Spark
        self.connection_definition = [
            {
                "name": "host",
            },
            {
                "name": "port",
                "type": "integer",
                "default": 32010
            },
            {
                "name": "use_encryption",
                "type": "boolean",
                "default": True
            },
            {
                "name": "disable_certificate_verification",
                "type": "boolean",
                "default": False
            },
            {
                "name": "username",
                "type": "string",
            },
            {
                "name": "password",
                "type": "string"
            }
        ]
        self.configuration_definition = [
            {"name": "query"},
        ]

    def get_data(self, configuration: dict, connection: dict):
        """ Get data from Dremio using Spark based on the provided configuration and connection details."""

        connection_string = f"jdbc:arrow-flight-sql://{connection['host']}:{connection['port']}/?useEncryption={str(connection['use_encryption']).lower()}&disableCertificateVerification={str(connection['disable_certificate_verification']).lower()}"
        
        df = (self.spark.read
            .format("jdbc")
            .option("driver", "org.apache.arrow.driver.jdbc.ArrowFlightJdbcDriver")
            .option("url", connection_string)
            .option("user", connection['username']) 
            .option("password", connection['password']) 
            .option("query", configuration["query"])
            .load())

        return df
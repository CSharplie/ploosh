"""
This module provides the SparkConfiguration class, which manages the creation and configuration
of Spark sessions based on YAML configuration files. It allows loading configurations, creating Spark
sessions, and assigning them to connectors.
"""

from pyspark.sql import SparkSession
import pathlib
import yaml


class sparkConfiguration:
    """
    Class to manage Spark session configurations and creation based on YAML configuration files.
    """
    connectors = None
    spark_configuration_path = None
    spark_configuration_filter = None
    spark_sessions = {}
    spark_sessions_configuration = {}


    def __init__(self, connectors: dict, spark_configuration_path: str, spark_configuration_filter: str)-> None:
        """
        Initialize SparkConfiguration with connectors and configuration file details.

        connectors                : dict: Dictionary containing connector objects
        :param spark_configuration_path  : str : Path to Spark configuration files
        :param spark_configuration_filter: str : File filter pattern for configuration files
        """
        self.connectors = connectors
        self.spark_configuration_path = spark_configuration_path
        self.spark_configuration_filter = spark_configuration_filter


    def get_config_files(self) -> None:
        """
        Reads YAML configuration files and stores Spark session configurations.
        """
        if self.spark_configuration_path is not None:
            spark_config_list = list(
                        pathlib.Path(self.spark_configuration_path).rglob(
                            self.spark_configuration_filter
                        )
                    )

            for file_path in spark_config_list:
                with open(file_path, encoding="UTF-8") as file:
                    configurations = yaml.load(file, Loader=yaml.loader.SafeLoader)
                    for connector_name, config in configurations.items():
                        self.spark_sessions_configuration[connector_name.upper()] = config


    def create_spark_sessions(self) -> None:
        """
        Creates Spark sessions based on loaded configurations.
        """
        self.get_config_files()
        for connector_name, spark_conf in self.spark_sessions_configuration.items():
            spark_builder = SparkSession.builder.appName(connector_name)
            for key, value in spark_conf.items():
                spark_builder = spark_builder.config(key, value)
            spark = spark_builder.getOrCreate()
            self.spark_sessions[connector_name] = spark
            spark = None


    def add_spark_sessions(self) -> dict:
        """
        Assigns Spark sessions to connectors if applicable.
        
        connectors : dict : Updated connectors dictionary with assigned Spark sessions
        """
        # Default spark session
        # Assigned to the spark connector if no spark configuration is mentioned by the user
        default_spark_session = SparkSession.builder \
                .master("local") \
                .appName("ploosh") \
                .getOrCreate()

        self.create_spark_sessions()

        if self.connectors:
            for connector_name in self.connectors.keys():
                if self.connectors[connector_name].is_spark:
                        if connector_name in self.spark_sessions.keys():
                            self.connectors[connector_name].spark = self.spark_sessions.get(connector_name)
                        else:
                            self.connectors[connector_name].spark = default_spark_session

        return self.connectors

"""Data connectors"""
from importlib import import_module
import inspect
import os


def get_connectors(spark_session):
    """Get all existing connectors"""

    connectors = {}

    # List all Python files in the current directory that start with "connector_"
    files = [
        name
        for name in os.listdir(os.path.dirname(__file__))
        if name.endswith(".py") and name.startswith("connector_")
    ]

    for file in files:
        module_name = file[:-3]  # Remove the ".py" extension to get the module name

        # Import the module dynamically
        for name, obj in inspect.getmembers(import_module(f"connectors.{module_name}")):
            if inspect.isclass(obj) and name.startswith("Connector"):
                current_connector = obj()  # Instantiate the connector class

                # If a Spark session is provided and the connector is Spark-based, set the Spark session
                if spark_session is not None and current_connector.is_spark:
                    current_connector.spark = spark_session

                # Add the connector to the connectors dictionary
                connectors[current_connector.name] = current_connector

    return connectors
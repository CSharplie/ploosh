"""Data connectors"""
from importlib import import_module
import inspect
import os

def get_connectors(spark_session):
    """Get all existing connectors"""

    connectors = {}

    files = [name for name in os.listdir(os.path.dirname(__file__)) if name.endswith(".py") and name.startswith("connector_")]
    for file in files:
        module_name = file[:-3]
        for name, obj in inspect.getmembers(import_module(f"connectors.{module_name}")):
            if inspect.isclass(obj) and name.startswith("Connector"):
                current_connector = obj()
                if spark_session is not None and current_connector.is_spark:
                    current_connector.spark = spark_session

                connectors[current_connector.name] = current_connector
    return connectors

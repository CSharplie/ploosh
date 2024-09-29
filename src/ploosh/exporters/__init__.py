"""Result exporter"""
from importlib import import_module
import os
import inspect


def get_exporters():
    """Get all existing exporters"""
    connectors = {}

    # List all Python files in the current directory that start with "exporter_"
    files = [
        name
        for name in os.listdir(os.path.dirname(__file__))
        if name.endswith(".py") and name.startswith("exporter_")
    ]

    for file in files:
        module_name = file[:-3]  # Remove the ".py" extension to get the module name

        # Import the module dynamically
        module = import_module(f"exporters.{module_name}")

        # Inspect the module to find classes that start with "Exporter"
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and name.startswith("Exporter"):
                current_connector = obj()  # Instantiate the exporter class
                connectors[
                    current_connector.name
                ] = current_connector  # Add the exporter to the connectors dictionary

    return connectors

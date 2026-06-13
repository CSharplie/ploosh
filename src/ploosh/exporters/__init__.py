"""Result exporter"""
from importlib import import_module
import os
import inspect


def get_exporters(connections={}, connectors={}):
    """Get all existing exporters"""
    exporters = {}

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
                current_exporter = obj()  # Instantiate the exporter class

                if current_exporter.name is None:
                    continue  # Skip if is the mother class Exporter without a defined name

                # Get the connection for the exporter if defined in the connections file by __export__ name
                connection = None
                if "__export__" in connections.keys() and connections["__export__"]["type"].upper() == current_exporter.name.upper():
                    connection = connections["__export__"]

                # Get the connector for the exporter if defined in the connectors
                # Will be used to execute the export query
                connector = None
                if current_exporter.name.upper() in connectors.keys():
                    connector = connectors[current_exporter.name.upper()]

                current_exporter.connection = connection
                current_exporter.connector = connector
                exporters[
                    current_exporter.name
                ] = current_exporter  # Add the exporter to the exporters dictionary

    return exporters

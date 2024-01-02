"""Data connectors"""
from importlib import import_module
import os
import inspect

def get_connectors():
    """Get all existings connectors"""
    connectors = {}

    files = [name for name in os.listdir(os.path.dirname(__file__)) if name.endswith(".py") and name.startswith("connector_")]
    for file in files:
        module_mame = file[:-3]
        for name, obj in inspect.getmembers(import_module(f"connectors.{module_mame}")):
            if inspect.isclass(obj) and name.startswith("Connector"):
                current_connector = obj()
                connectors[current_connector.name] = current_connector
    return connectors

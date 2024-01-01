"""Data connectors"""
import sys
import inspect
from connectors.connector_mssql import ConnectorMSSQL
from connectors.connector_csv import ConnectorCSV

def get_connectors():
    """Get all existings connectors"""
    connectors = {}
    for name, obj in inspect.getmembers(sys.modules["connectors"]):
        if inspect.isclass(obj) and name.startswith("Connector"):
            current_connector = obj()
            connectors[current_connector.name] = current_connector
    return connectors

"""Result exporter"""
import sys
import inspect
from exporters.exporter_json import ExporterJSON
from exporters.exporter_csv import ExporterCSV
from exporters.exporter_trx import ExporterTRX

def get_exporters():
    """Get all existings exporters"""

    exporters = {}
    for name, obj in inspect.getmembers(sys.modules["exporters"]):
        if inspect.isclass(obj) and name.startswith("Exporter"):
            current_exporter = obj()
            exporters[current_exporter.name] = current_exporter
    return exporters

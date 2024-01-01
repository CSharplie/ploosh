# pylint: disable=R0903,W0613
"""Test result exporter"""
from datetime import datetime

class Exporter:
    """Test result exporter"""
    name = None
    output_path = None

    @staticmethod
    def date_to_string(data):
        """Convert datetime ton string"""
        if not isinstance(data, datetime):
            return None

        return data.strftime("%Y-%m-%dT%H:%M:%SZ")

    def export(self, cases:dict):
        """Export to destination"""
        return None

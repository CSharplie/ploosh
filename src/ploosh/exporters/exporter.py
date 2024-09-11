# pylint: disable=R0903,W0613
"""Test result exporter"""
from datetime import datetime


class Exporter:
    """Test result exporter"""
    name = None  # Name of the exporter
    output_path = None  # Output path for the exported results

    @staticmethod
    def date_to_string(data):
        """Convert datetime to string in ISO 8601 format"""
        if not isinstance(data, datetime):
            return None

        return data.strftime("%Y-%m-%dT%H:%M:%SZ")

    def export(self, cases: dict):
        """Export test case results to the destination"""
        return None

"""Export test case result to CSV format"""
import csv
import os
from exporters.exporter import Exporter

class ExporterCSV(Exporter):
    """Export test case result to CSV format"""

    def __init__(self):
        self.name = "CSV"

    def export(self, cases:dict):
        """Export test case"""

        output_file = f"{self.output_path}/csv/test_results.csv"

        data = [[
               "name",
               "state",
               "source_start",
               "source_end",
               "source_duration",
               "expected_start",
               "expected_end",
               "expected_duration",
               "compare_start",
               "compare_end",
               "compare_duration",
               "error_type",
               "error_message",
        ]]
        for name in cases:
            case = cases[name]

            case_data = [
                name,
                case.state,
                Exporter.date_to_string(case.source.duration.start),
                Exporter.date_to_string(case.source.duration.end),
                case.source.duration.duration,
                Exporter.date_to_string(case.expected.duration.start),
                Exporter.date_to_string(case.expected.duration.end),
                case.expected.duration.duration,
                Exporter.date_to_string(case.compare_duration.start),
                Exporter.date_to_string(case.compare_duration.end),
                case.compare_duration.duration,
                case.error_type,
                case.error_message,
            ]

            data.append(case_data)

        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, "w", encoding="UTF-8") as f:
            writer = csv.writer(f, lineterminator="\n")
            writer.writerows(data)
            f.close()

"""Export test case result to CSV format"""
import csv
import os
from exporters.exporter import Exporter

class ExporterCSV(Exporter):
    """Export test case result to CSV format"""

    def __init__(self):
        # Set the name of the exporter
        self.name = "CSV"

    def export(self, cases: dict):
        """Export test case results to a CSV file"""

        # Define the output file path
        output_file = f"{self.output_path}/csv/test_results.csv"

        # Initialize the data list with headers
        data = [[
            "name",
            "state",
            "source_start",
            "source_end",
            "source_duration",
            "source_count",
            "expected_start",
            "expected_end",
            "expected_duration",
            "expected_count",
            "compare_start",
            "compare_end",
            "compare_duration",
            "success_rate",
            "error_type",
            "error_message",
        ]]

        # Iterate over each test case and collect data
        for name in cases:
            case = cases[name]

            # Collect data for the current test case
            case_data = [
                name,
                case.state,
                Exporter.date_to_string(case.source.duration.start),
                Exporter.date_to_string(case.source.duration.end),
                case.source.duration.duration,
                case.source.count,
                Exporter.date_to_string(case.expected.duration.start),
                Exporter.date_to_string(case.expected.duration.end),
                case.expected.duration.duration,
                case.expected.count,
                Exporter.date_to_string(case.compare_duration.start),
                Exporter.date_to_string(case.compare_duration.end),
                case.compare_duration.duration,
                case.success_rate,
                case.error_type,
                case.error_message,
            ]

            # Append the collected data to the data list
            data.append(case_data)

            # If there is a comparison gap, export it to an Excel file
            if case.df_compare_gap is not None:
                detail_file_path = f"{self.output_path}/json/test_results/{name}.xlsx"

                # Create directories if they do not exist
                os.makedirs(os.path.dirname(detail_file_path), exist_ok=True)
                case.df_compare_gap.to_excel(detail_file_path)

        # Create directories if they do not exist
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        # Write the collected data to the CSV file
        with open(output_file, "w", encoding="UTF-8") as f:
            writer = csv.writer(f, lineterminator="\n")
            writer.writerows(data)
            f.close()

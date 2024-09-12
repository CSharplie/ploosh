"""Export test case result to JSON format"""

import json
import os
from exporters.exporter import Exporter


class ExporterJSON(Exporter):
    """Export test case result to JSON format"""

    def __init__(self):
        # Set the name of the exporter
        self.name = "JSON"

    def export(self, cases: dict):
        """Export test case results to a JSON file"""

        # Define the output file path
        output_file = f"{self.output_path}/json/test_results.json"

        data = []
        # Iterate over each test case and collect data
        for name in cases:
            case = cases[name]

            # Collect basic data for the current test case
            case_data = {
                "name": name,
                "state": case.state,
            }

            # Collect source data if available
            if case.source.duration.start is not None:
                case_data["source"] = {
                    "start": Exporter.date_to_string(case.source.duration.start),
                    "end": Exporter.date_to_string(case.source.duration.end),
                    "duration": case.source.duration.duration,
                    "count": case.source.count,
                }

            # Collect expected data if available
            if case.expected.duration.start is not None:
                case_data["expected"] = {
                    "start": Exporter.date_to_string(case.expected.duration.start),
                    "end": Exporter.date_to_string(case.expected.duration.end),
                    "duration": case.expected.duration.duration,
                    "count": case.expected.count,
                }

            # Collect comparison data if available
            if case.compare_duration.start is not None:
                case_data["compare"] = {
                    "start": Exporter.date_to_string(case.compare_duration.start),
                    "end": Exporter.date_to_string(case.compare_duration.end),
                    "duration": case.compare_duration.duration,
                    "success_rate": case.success_rate,
                }

            # Collect error data if the test case failed or encountered an error
            if case.state in ["error", "failed"]:
                case_data["error"] = {
                    "type": case.error_type,
                    "message": case.error_message,
                }

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

        # Write the collected data to the JSON file
        with open(output_file, "w", encoding="UTF-8") as f:
            f.write(json.dumps(data, indent=2))

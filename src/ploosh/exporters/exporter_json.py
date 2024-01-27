"""Export test case result to JSON format"""

import json
from exporters.exporter import Exporter

class ExporterJSON(Exporter):
    """Export test case result to JSON format"""

    def __init__(self):
        self.name = "JSON"

    def export(self, cases:dict):
        """Export test case"""

        output_file = f"{self.output_path}/json/test_results.json"

        data = []
        for name in cases:
            case = cases[name]

            case_data = {
                "name": name,
                "state": case.state,
            }

            if case.source.duration.start is not None:
                case_data["source"] = {
                    "start": Exporter.date_to_string(case.source.duration.start),
                    "end":  Exporter.date_to_string(case.source.duration.end),
                    "duration":  case.source.duration.duration,
                }

            if case.expected.duration.start is not None:
                case_data["expected"] = {
                    "start": Exporter.date_to_string(case.expected.duration.start),
                    "end":  Exporter.date_to_string(case.expected.duration.end),
                    "duration":  case.expected.duration.duration,
                }

            if case.compare_duration.start is not None:
                case_data["compare"] = {
                    "start": Exporter.date_to_string(case.compare_duration.start),
                    "end": Exporter.date_to_string(case.compare_duration.end),
                    "duration": case.compare_duration.duration,
                }

            if case.state != "passed":
                case_data["error"] = {
                    "type": case.error_type,
                    "message": case.error_message
                }

            data.append(case_data)

        with open(output_file, "w", encoding="UTF-8") as f:
            f.write(json.dumps(data, indent=2))

import sys
import yaml, os, pathlib
from sys import path
from pathlib import Path
from datetime import datetime

run_path = os.path.dirname(__file__)
root_directory = os.path.abspath(f"{run_path}/../")
path.append(f"{root_directory}/framework/resources")

from core.miscellaneous import print_log
from core.configuration import get_connections, get_test_cases, get_settings
from core.compare import get_aborted_object
from core.loader import load_data_from_source
from core.compare import compare_dataframes
from core.export import export_test_results

connections = get_connections(root_directory, sys.argv[1:])
test_cases = get_test_cases(root_directory)
settings = get_settings(root_directory)

all_results = []
for test_name in test_cases:
    print_log(f"Execute '{test_name}'")
    current_test_case = test_cases[test_name]

    if "source" not in current_test_case.keys():
        raise "03x001 - The 'source' is not defined for the current test case"
    if "expected" not in current_test_case.keys():
        raise "03x002 - The 'expected' is not defined for the current test case"

    compare_options = None
    if "compare_options" in current_test_case.keys():
        compare_options = current_test_case["compare_options"]

    start_time = datetime.now()
    try:
        print_log("Load source dataset")
        source = load_data_from_source(current_test_case["source"], connections)

        print_log("Load expected dataset")
        expected = load_data_from_source(current_test_case["expected"], connections)

        print_log("Compare source dataset and expected dataset")
        result = compare_dataframes(test_name, source["df_data"], expected["df_data"], compare_options)
        result["source_duration"] = source["duration"]
        result["expected_duration"] = expected["duration"]

        all_results.append(result)
    except Exception as e:
        all_results.append(get_aborted_object(test_name, start_time, str(e)))
        print_log(str(e), 40)

print_log("Export results")
export_test_results(root_directory, settings, all_results)

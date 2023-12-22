import sys
from datetime import datetime
from core import *

connections = get_connections(ROOT_DIRECTORY, sys.argv[1:])
test_cases = get_test_cases(ROOT_DIRECTORY)
settings = get_settings(ROOT_DIRECTORY)

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
export_test_results(ROOT_DIRECTORY, settings, all_results)

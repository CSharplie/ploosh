"""Automatized Testing Framework"""

import sys
from logs import Log
from connectors import get_connectors
from exporters import get_exporters
from parameters import Parameters
from configuration import Configuration

def load_data(current_case, process_type):
    """load data from source or expected"""

    try:
        current_case.load_data(process_type)
        return True
    except Exception as e:
        current_case.load_data_error(process_type, str(e))
        current_case.calculate_durations()
        Log.print_error(str(e))

    return False

def compare_data(current_case):
    """Compare data between source and expected"""

    try:
        current_case.compare_dataframes()
        return True
    except Exception as e:
        current_case.compare_dataframes_error(str(e))
        current_case.calculate_durations()
        Log.print_error(str(e))

    return False

def main():
    """Main function"""

    Log.print("Initialization")
    connectors = get_connectors()
    exporters = get_exporters()
    parameters = Parameters(sys.argv)
    configuration = Configuration(parameters, connectors, exporters)
    cases = configuration.get_cases()

    Log.print("Start processing tests cases")
    for i, case_name in enumerate(cases):
        Log.print(f"Process test case '{case_name}' ({i + 1}/{len(cases)})")
        current_case = cases[case_name]

        Log.print("Load source data")
        if not load_data(current_case, "source"):
            continue

        Log.print("Load expected data")
        if not load_data(current_case, "expected"):
            continue

        Log.print("Compare source and expected data")
        if not compare_data(current_case):
            continue

        Log.print(f"Compare state: {current_case.state}")

        current_case.calculate_durations()

    Log.print("Export results")
    configuration.exporter.export(cases)

if __name__ == "__main__":
    main()

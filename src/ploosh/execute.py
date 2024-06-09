"""Automatized Testing Framework"""

import sys
from colorama import Fore, Style
from pyspark.sql import SparkSession
from case import StateStatistics
from logs import Log, print_compare_state, print_summary
from connectors import get_connectors
from exporters import get_exporters
from parameters import Parameters
from configuration import Configuration

def load_data(current_case, process_type, statistics):
    """load data from source or expected"""

    try:
        current_case.load_data(process_type)
        return True
    except Exception as e:
        current_case.load_data_error(process_type, str(e))
        current_case.calculate_durations()
        statistics.add_state(current_case.state)
        Log.print_error(str(e))

    return False

def compare_data(current_case, statistics, spark_session):
    """Compare data between source and expected"""

    try:
        if current_case.source.connector.is_spark and current_case.expected.connector.is_spark:
            current_case.compare_dataframes_with_spark(spark_session)
        else:
            current_case.compare_dataframes()
        statistics.add_state(current_case.state)
        return True
    except Exception as e:
        current_case.compare_dataframes_error(str(e))
        current_case.calculate_durations()
        statistics.add_state(current_case.state)
        Log.print_error(str(e))

    return False

def execute(args=None, spark_session=None):
    """Main function"""

    Log.init()
    Log.print_logo()

    statistics = StateStatistics()

    Log.print(f"{Fore.CYAN}Initialization[...]")
    try:
        if args is None:
            parameters = Parameters(sys.argv)
        else:
            parameters = Parameters(args)

        if parameters.spark_mode is True and spark_session is None:
            Log.print("Start spark session")
            spark_session = SparkSession.builder \
                .master("local") \
                .appName("ploosh") \
                .getOrCreate()

        Log.print("Load connectors")
        connectors = get_connectors(spark_session)
        Log.print("Load exporters")
        exporters = get_exporters()

        Log.print("Load configuration")
        configuration = Configuration(parameters, connectors, exporters)
        cases = configuration.get_cases()
    except Exception as e:
        Log.print_error(str(e))
        exit(1)

    Log.print(f"{Fore.CYAN}Start processing tests cases[...]")
    for i, case_name in enumerate(cases):
        current_case = cases[case_name]
        
        if current_case.disabled:
            Log.print(f"{Fore.MAGENTA}{case_name} [...] ({i + 1}/{len(cases)}) - Skipped")
            statistics.add_state(current_case.state)
            continue

        Log.print(f"{Fore.MAGENTA}{case_name} [...] ({i + 1}/{len(cases)}) - Started")

        Log.print("Load source data")
        if not load_data(current_case, "source", statistics):
            continue

        Log.print("Load expected data")
        if not load_data(current_case, "expected", statistics):
            continue

        Log.print("Compare source and expected data")
        if not compare_data(current_case, statistics, spark_session):
            continue

        print_compare_state(current_case)

        current_case.calculate_durations()

    Log.print(f"{Fore.CYAN}Export results[...]")
    configuration.exporter.export(cases)
    Log.print(f"{Fore.CYAN}Summary[...]")

    print_summary(cases, statistics)

    if statistics.error > 0 and parameters.failure_on_error:
        exit(1)
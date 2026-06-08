"""Automatized Testing Framework"""

import sys
import uuid
from concurrent.futures import ThreadPoolExecutor
from case import StateStatistics
from connectors import get_connectors
from exporters import get_exporters
from parameters import Parameters
from configuration import Configuration
from logs import Log, print_compare_state, print_summary


def load_data(current_case_name, current_case, process_type, statistics):
    """Load data from source or expected"""
    try:
        # Spark sessions are thread-safe for concurrent job submission, so loads
        # can run in parallel across workers without serializing on a shared lock.
        current_case.load_data(process_type)
        return True
    except Exception as e:
        # Handle any errors that occur during data loading
        current_case.load_data_error(process_type, str(e))
        current_case.calculate_durations()
        statistics.add_state(current_case.state)
        error_message = f"{current_case_name}\nLoading {process_type} error:\n{str(e)}"
        Log.print_error(error_message)
    return False


def compare_data(current_case_name, current_case, statistics, spark_session):
    """Compare data between source and expected"""
    try:
        # Compare data using Spark if both connectors are Spark-based
        if current_case.source.connector.is_spark and current_case.expected.connector.is_spark:
            # Spark sessions handle concurrent jobs, so compares run in parallel too.
            current_case.compare_dataframes_with_spark(spark_session)
        else:
            # Otherwise, use a standard comparison
            current_case.compare_dataframes()
        statistics.add_state(current_case.state)
        return True
    except Exception as e:
        # Handle any errors that occur during data comparison
        current_case.compare_dataframes_error(str(e))
        current_case.calculate_durations()
        statistics.add_state(current_case.state)
        error_message = f"{current_case_name}\nData comparison error:\n{str(e)}"
        Log.print_error(error_message)
    return False


def process_case(current_case, case_name, statistics, spark_session):
    """Process a single test case: load, compare and compute durations"""
    # Skip disabled test cases
    if current_case.disabled:
        Log.print_case_progress(case_name, state="notExecuted")
        statistics.add_state(current_case.state)
        return

    Log.print_case_progress(case_name, state="progress")

    if not load_data(case_name,current_case, "source", statistics):
        Log.print_case_progress(case_name, state=current_case.state)
        return

    if not load_data(case_name, current_case, "expected", statistics):
        Log.print_case_progress(case_name, state=current_case.state)
        return

    if not compare_data(case_name, current_case, statistics, spark_session):
        Log.print_case_progress(case_name, state=current_case.state)
        return

    # Print comparison state and calculate durations
    print_compare_state(case_name, current_case)
    Log.print_case_progress(case_name, state=current_case.state)

    current_case.calculate_durations()


def execute(args=None, spark_session=None):
    """Main function to execute test cases"""
    Log.init()
    Log.print_logo()

    statistics = StateStatistics()
    execution_id = str(uuid.uuid4())

    Log.print_message("Initialization " + "=" * 200, no_overflow=True, style="bold blue")
    try:
        # Parse command-line arguments
        if args is None:
            parameters = Parameters(sys.argv)
        else:
            parameters = Parameters(args)

        # Initialize Spark session if needed
        if parameters.spark_mode is True and spark_session is None:
            from pyspark.sql import SparkSession  # pylint: disable=C0415

            Log.print_message("Start spark session")
            spark_session = SparkSession.builder \
                .master("local") \
                .appName("ploosh") \
                .getOrCreate()

        # Load connectors and exporters
        Log.print_message("Load connectors")
        connectors = get_connectors(spark_session)
        Log.print_message("Load exporters")
        exporters = get_exporters()

        # Load configuration and test cases
        Log.print_message("Load configuration")
        configuration = Configuration(parameters, connectors, exporters)
        cases = configuration.get_cases()
    except Exception as e:
        # Handle any errors that occur during initialization
        Log.print_error(str(e))
        sys.exit(1)

    Log.print_message("Start processing tests cases " + "=" * 200, no_overflow=True, style="bold blue")

    if parameters.workers > 1:
        # Process test cases in parallel using a thread pool
        with ThreadPoolExecutor(max_workers=parameters.workers) as executor:
            futures = [
                executor.submit(
                    process_case,
                    cases[case_name],
                    case_name,
                    statistics,
                    spark_session,
                )
                for case_name in cases
            ]
            # Wait for completion and propagate unexpected errors
            for future in futures:
                future.result()
    else:
        # Process test cases sequentially
        for case_name in cases:
            process_case(
                cases[case_name],
                case_name,
                statistics,
                spark_session,
            )

    # Export test results
    configuration.exporter.export(cases, execution_id)
    Log.print_message("Summary " + "=" * 200, no_overflow=True, style="bold blue")
    # Print summary of test results
    print_summary(cases, statistics)

    # Exit with error code if there were errors and failure_on_error is set
    if statistics.error > 0 and parameters.failure_on_error:
        Log.print_message("Exiting due to errors", "ERROR")
        sys.exit(1)

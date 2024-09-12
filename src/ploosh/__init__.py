"""Initialization for command line"""

import os
import sys

# Add the current directory to the system path
sys.path.append(os.path.dirname(__file__))

from execute import execute


def execute_cases(
    cases=None,
    connections=None,
    spark=None,
    spark_session=None,
    filter=None,
    path_output=None,
):
    """Execute test cases with the given parameters"""
    args = ["ploosh"]

    # Add cases parameter to arguments if provided
    if cases is not None:
        args.append("--cases")
        args.append(cases)

    # Add connections parameter to arguments if provided
    if connections is not None:
        args.append("--connections")
        args.append(connections)

    # Add spark parameter to arguments if provided
    if spark is not None:
        args.append("--spark")
        args.append(spark)

    # Add filter parameter to arguments if provided
    if filter is not None:
        args.append("--filter")
        args.append(filter)

    # Add output path parameter to arguments if provided
    if path_output is not None:
        args.append("--output")
        args.append(path_output)

    # Execute the test cases with the constructed arguments
    execute(args, spark_session)

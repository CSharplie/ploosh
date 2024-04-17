"""Initialization for command line"""

import os
import sys

sys.path.append(os.path.dirname(__file__))

from execute import execute

def execute_cases(cases = None, connections = None, spark = None, spark_session = None, filter = None, path_output = None):
    args = ["ploosh"]

    if cases is not None:
        args.append("--cases")
        args.append(cases)

    if connections is not None:
        args.append("--connections")
        args.append(connections)

    if spark is not None:
        args.append("--spark")
        args.append(spark)

    if filter is not None:
        args.append("--filter")
        args.append(filter)

    if path_output is not None:
        args.append("--output")
        args.append(path_output)

    execute(args, spark_session)
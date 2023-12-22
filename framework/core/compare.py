from datetime import datetime
import pandas as pd


def compare_dataframes(test_name, df_source, df_expected, compare_options):
    error_message = None
    error_type = None
    df_details = None

    start_time = datetime.now()

    count_source = len(df_source)
    count_expected = len(df_expected)

    if count_source != count_expected:
        error_type = "Count"
        error_message = f"The count in source dataset ({count_source}) is differant than the count the in expected dataset ({count_expected})"

    if error_message is None and count_source != 0:
        if compare_options is not None and compare_options["ignore"] is not None:
            df_source = df_source.drop(columns = compare_options["ignore"], axis = 1, errors = "ignore")
            df_expected = df_expected.drop(columns = compare_options["ignore"], axis = 1, errors = "ignore")

        df_columns_source = pd.DataFrame({ "columns": df_source.columns }).sort_values(by = ["columns"]).reset_index()
        df_columns_expected = pd.DataFrame({ "columns": df_expected.columns }).sort_values(by = ["columns"]).reset_index()

        message = f"The headers are differant between source dataset and expected dataset"
        if len(df_columns_source) != len(df_columns_expected):
            error_message = message
            error_type = "Headers"
        else:
            df_compare = df_columns_source.compare(df_columns_expected, result_names = ("source", "expected"))
            if len(df_compare) != 0 :
                error_message = message
                error_type = "Headers"
                df_details = df_compare

    if error_message is None and count_source != 0:
        if compare_options is not None and compare_options["sort"] is not None:
            df_source = df_source.sort_values(by = compare_options["sort"]).reset_index()
            df_expected = df_expected.sort_values(by = compare_options["sort"]).reset_index()

        df_compare = df_source.compare(df_expected, result_names = ("source", "expected"))
        if len(df_compare) != 0 :
            error_message = "Some rows are not equals between source dataset and expected dataset"
            df_details = df_compare
            error_type = "Data"

    end_time = datetime.now()
    duration = (end_time - start_time).microseconds / 60000000

    if error_message is None:
        state = "passed"
    else:
        state = "failed"

    return {
        "start_time" : start_time,
        "end_time" : end_time,
        "test_name" : test_name,
        "state" : state,
        "error_type" : error_type,
        "error_message" : error_message,
        "compare_duration" : duration,
        "unknow_duration" : 0,
        "df_details" : df_details,
    }


def get_aborted_object(test_name, start_time, error_message):
    current_datetime = datetime.now()
    end_time = datetime.now()
    duration = (end_time - start_time).microseconds / 60000000

    return {
        "start_time" : start_time,
        "end_time" : end_time,
        "test_name" : test_name,
        "state" : "aborted",
        "error_message" : error_message,
        "error_type" : "Technical",
        "source_duration" : 0,
        "expected_duration" : 0,
        "compare_duration" : 0,
        "unknow_duration" : duration,
        "df_details" : None
    }

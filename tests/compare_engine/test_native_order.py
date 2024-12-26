import pandas as pd
import pytest
from pyjeb import control_and_setup
from ploosh.compare_engine_native import CompareEngineNative
from ploosh.configuration import Configuration

@pytest.fixture
def controls():
    controls = Configuration.case_definition
    controls = [control for control in controls if control["name"].startswith("options")]
    return controls

def test_success(controls):
    df_source = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
    df_expected = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
    parameters = {}
    options = control_and_setup(parameters, controls)["options"]

    compare_engine = CompareEngineNative(df_source, df_expected, options)
    assert compare_engine.compare()
    assert compare_engine.error_type is None

def test_mismatches_headers(controls):
    df_source = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
    df_expected = pd.DataFrame({"A": [1, 2, 3], "C": [4, 5, 6]})
    parameters = {}
    options = control_and_setup(parameters, controls)["options"]

    compare_engine = CompareEngineNative(df_source, df_expected, options)
    assert not compare_engine.compare()
    assert compare_engine.error_type == "headers"

def test_header_case_insensitive(controls):
    df_source = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
    df_expected = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    parameters = {}
    options = control_and_setup(parameters, controls)["options"]

    compare_engine = CompareEngineNative(df_source, df_expected, options)
    assert compare_engine.compare()
    assert compare_engine.error_type is None

def test_header_ignore(controls):
    df_source = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
    df_expected = pd.DataFrame({"A": [1, 2, 3], "C": [4, 5, 6]})
    parameters = {
        "options": {
            "ignore": ["C"]
        }
    }
    options = control_and_setup(parameters, controls)["options"]

    compare_engine = CompareEngineNative(df_source, df_expected, options)
    assert compare_engine.compare()
    assert compare_engine.error_type is None


def test_count_failure(controls):
    df_source = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
    df_expected = pd.DataFrame({"A": [1, 2], "B": [4, 5]})
    parameters = {}
    options = control_and_setup(parameters, controls)["options"]

    compare_engine = CompareEngineNative(df_source, df_expected, options)
    assert not compare_engine.compare()
    assert compare_engine.error_type == "count"

def test_data_mismatch(controls):
    df_source = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
    df_expected = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 7]})
    parameters = {}
    options = control_and_setup(parameters, controls)["options"]

    compare_engine = CompareEngineNative(df_source, df_expected, options)
    assert not compare_engine.compare()
    assert compare_engine.error_type == "data"

def test_data_mismatch_ignore(controls):
    df_source = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
    df_expected = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 7]})
    parameters = {
        "options": {
            "ignore": ["B"]
        }
    }
    options = control_and_setup(parameters, controls)["options"]

    compare_engine = CompareEngineNative(df_source, df_expected, options)
    assert compare_engine.compare()
    assert compare_engine.error_type is None

def test_data_case_insensitive(controls):
    df_source = pd.DataFrame({"A": ["TOTO", "TITI", "TATA"], "B": ["COCO", "CICI", "CACA"]})
    df_expected = pd.DataFrame({"A": ["toto", "titi", "tata"], "B": ["coco", "cici", "caca"]})
    parameters = {
        "options": {
            "ignore": ["B"],
            "case_insensitive": True
        }
    }
    options = control_and_setup(parameters, controls)["options"]

    compare_engine = CompareEngineNative(df_source, df_expected, options)
    assert compare_engine.compare()
    assert compare_engine.error_type is None

def test_data_case_insensitive_failure(controls):
    df_source = pd.DataFrame({"A": ["TOTO", "TITI", "TATA"], "B": ["COCO", "CICI", "CACA"]})
    df_expected = pd.DataFrame({"A": ["toto", "titi", "tata"], "B": ["coco", "cici", "caca"]})
    parameters = {
        "options": {
            "ignore": ["B"],
            "case_insensitive": False
        }
    }
    options = control_and_setup(parameters, controls)["options"]

    compare_engine = CompareEngineNative(df_source, df_expected, options)
    assert not compare_engine.compare()
    assert compare_engine.error_type == "data"
    

def test_data_trim(controls):
    df_source = pd.DataFrame({"A": ["TOTO ", " TITI", "TATA "], "B": ["COCO", "CICI ", " CACA"]})
    df_expected = pd.DataFrame({"A": ["TOTO", "TITI", "TATA"], "B": ["COCO", "CICI", "CACA"]})
    parameters = {
        "options": {
            "trim": True
        }
    }
    options = control_and_setup(parameters, controls)["options"]

    compare_engine = CompareEngineNative(df_source, df_expected, options)
    assert compare_engine.compare()
    assert compare_engine.error_type is None

def test_data_trim_failure(controls):
    df_source = pd.DataFrame({"A": ["TOTO ", " TITI", "TATA "], "B": ["COCO", "CICI ", " CACA"]})
    df_expected = pd.DataFrame({"A": ["TOTO", "TITI", "TATA"], "B": ["COCO", "CICI", "CACA"]})
    parameters = {
        "options": {
            "trim": False
        }
    }
    options = control_and_setup(parameters, controls)["options"]

    compare_engine = CompareEngineNative(df_source, df_expected, options)
    assert not compare_engine.compare()
    assert compare_engine.error_type == "data"

def test_data_tolerance(controls):
    df_source = pd.DataFrame({"A": [1.0, 2.0, 3.0], "B": [4.0, 5.0, 6.0]})
    df_expected = pd.DataFrame({"A": [1.0, 2.0, 3.0], "B": [4.0, 5.0, 6.1]})
    parameters = {
        "options": {
            "tolerance": 0.1
        }
    }
    options = control_and_setup(parameters, controls)["options"]

    compare_engine = CompareEngineNative(df_source, df_expected, options)
    assert compare_engine.compare()
    assert compare_engine.error_type is None

def test_data_tolerance_failure(controls): 
    df_source = pd.DataFrame({"A": [1.0, 2.0, 3.0], "B": [4.0, 5.0, 6.0]})
    df_expected = pd.DataFrame({"A": [1.0, 2.0, 3.0], "B": [4.0, 5.0, 6.1]})
    parameters = {
        "options": {
            "tolerance": 0.01
        }
    }
    options = control_and_setup(parameters, controls)["options"]

    compare_engine = CompareEngineNative(df_source, df_expected, options)
    assert not compare_engine.compare()
    assert compare_engine.error_type == "data"

def test_data_sort(controls):
    df_source = pd.DataFrame({"A": [1, 3, 2], "B": [4, 6, 5]})
    df_expected = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
    parameters = {
        "options": {
            "sort": ["A"]
        }
    }
    options = control_and_setup(parameters, controls)["options"]

    compare_engine = CompareEngineNative(df_source, df_expected, options)
    assert compare_engine.compare()
    assert compare_engine.error_type is None

def test_data_sort_failure(controls):
    df_source = pd.DataFrame({"A": [1, 3, 2], "B": [4, 5, 6]})
    df_expected = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
    parameters = {
        "options": {
            "sort": ["B"]
        }
    }
    options = control_and_setup(parameters, controls)["options"]

    compare_engine = CompareEngineNative(df_source, df_expected, options)
    assert not compare_engine.compare()
    assert compare_engine.error_type == "data"

def test_empty_dataframes(controls):
    df_source = pd.DataFrame({"A": [], "B": []})
    df_expected = pd.DataFrame({"A": [], "B": []})
    parameters = {}
    options = control_and_setup(parameters, controls)["options"]

    compare_engine = CompareEngineNative(df_source, df_expected, options)
    assert compare_engine.compare()
    assert compare_engine.error_type is None

def test_empty_dataframes_failure(controls):
    df_source = pd.DataFrame({"A": [], "B": []})
    df_expected = pd.DataFrame({"A": [], "B": []})
    parameters = {
        "options": {
            "allow_no_rows": False
        }
    }
    options = control_and_setup(parameters, controls)["options"]

    compare_engine = CompareEngineNative(df_source, df_expected, options)
    assert not compare_engine.compare()
    assert compare_engine.error_type == "data"

def test_empty_dataframes_asymetric(controls):
    df_source = pd.DataFrame({"A": [], "B": []})
    df_expected = pd.DataFrame()
    parameters = {}
    options = control_and_setup(parameters, controls)["options"]

    compare_engine = CompareEngineNative(df_source, df_expected, options)
    assert compare_engine.compare()

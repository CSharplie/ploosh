import pandas as pd
import pytest
from pyjeb import control_and_setup
from ploosh.engines.load_engine_native import LoadEngineNative
from ploosh.configuration import Configuration

@pytest.fixture
def controls():
    controls = Configuration.case_definition
    controls = [control for control in controls if control["name"].startswith("options")]
    return controls

def test_count(controls):
    df_data = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
    parameters = {}
    options = control_and_setup(parameters, controls)["options"]

    load_engine = LoadEngineNative(None, options, None)
    df_data = load_engine.execute(df_data)
    assert load_engine.count == 3

def test_cast_datetime(controls):
    df_data = pd.DataFrame({"A": [1, 2, 3], "B": ["2021-01-01", "2021-01-02", "2021-01-03"]})
    parameters = {
        "options": {
            "cast": [
                {
                    "name": "B",
                    "type": "datetime"
                }
            ]
        }
    }
    options = control_and_setup(parameters, controls)["options"]

    load_engine = LoadEngineNative(None, options, None)
    df_data = load_engine.execute(df_data)
    assert df_data["B"].dtype == "datetime64[ns]"
    assert df_data["A"].dtype == "int64"

def test_cast_int(controls):
    df_data = pd.DataFrame({"A": [1, 2, 3], "B": ["4", "5", "6"]})
    parameters = {
        "options": {
            "cast": [
                {
                    "name": "B",
                    "type": "int"
                }
            ]
        }
    }
    options = control_and_setup(parameters, controls)["options"]

    load_engine = LoadEngineNative(None, options, None)
    df_data = load_engine.execute(df_data)
    assert df_data["B"].dtype == "int64"
    assert df_data["A"].dtype == "int64"

def test_cast_float(controls):
    df_data = pd.DataFrame({"A": [1, 2, 3], "B": ["4.0", "5.0", "6.0"]})
    parameters = {
        "options": {
            "cast": [
                {
                    "name": "B",
                    "type": "float"
                }
            ]
        }
    }
    options = control_and_setup(parameters, controls)["options"]

    load_engine = LoadEngineNative(None, options, None)
    df_data = load_engine.execute(df_data)
    assert df_data["B"].dtype == "float64"
    assert df_data["A"].dtype == "int64"
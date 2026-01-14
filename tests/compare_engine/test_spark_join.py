from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType
import pytest
from pyjeb import control_and_setup
from ploosh.engines.compare_engine_spark import CompareEngineSpark
from ploosh.configuration import Configuration

@pytest.fixture
def controls():
    controls = Configuration.case_definition
    controls = [control for control in controls if control["name"].startswith("options")]
    return controls

@pytest.fixture
def spark():
    return SparkSession.builder \
        .appName("ploosh") \
        .master("spark://localhost:7077") \
        .config("spark.executor.memory", "1g") \
        .config("spark.driver.memory", "1g") \
        .getOrCreate()

def test_success(spark, controls):
    df_source = spark.createDataFrame([(1, 4, "X"), (2, 5, "Y"), (3, 6, "Z")], ["A", "B", "J"])
    df_expected = spark.createDataFrame([(3, 6, "Z"), (2, 5, "Y"), (1, 4, "X")], ["A", "B", "J"])

    parameters = {
        "options": {
            "compare_mode": "join",
            "join_keys": ["J"]
        }
    }
    options = control_and_setup(parameters, controls)["options"]

    compare_engine = CompareEngineSpark(df_source, df_expected, options)
    assert compare_engine.compare()
    assert compare_engine.error_type is None

def test_mismatches_headers(spark, controls):
    df_source = spark.createDataFrame([(1, 4), (2, 5), (3, 6)], ["A", "B"])
    df_expected = spark.createDataFrame([(1, 4), (2, 5), (3, 6)], ["A", "C"])

    parameters = {
        "options": {
            "compare_mode": "join"
        }
    }
    options = control_and_setup(parameters, controls)["options"]

    compare_engine = CompareEngineSpark(df_source, df_expected, options)
    assert not compare_engine.compare()
    assert compare_engine.error_type == "headers"

def test_header_case_insensitive(spark, controls):
    df_source = spark.createDataFrame([(1, 4, "X"), (2, 5, "Y"), (3, 6, "Z")], ["a", "b", "j"])
    df_expected = spark.createDataFrame([(3, 6, "Z"), (2, 5, "Y"), (1, 4, "X")], ["A", "B", "J"])

    parameters = {
        "options": {
            "compare_mode": "join",
            "join_keys": ["J"]
        }
    }
    options = control_and_setup(parameters, controls)["options"]

    compare_engine = CompareEngineSpark(df_source, df_expected, options)
    assert compare_engine.compare()
    assert compare_engine.error_type is None

def test_header_ignore(spark, controls):
    df_source = spark.createDataFrame([(1, 4, 10, "X"), (2, 5, 11, "Y"), (3, 6, 12, "Z")], ["a", "b", "c", "j"])
    df_expected = spark.createDataFrame([(3, 6, 13, "Z"), (2, 5, 14, "Y"), (1, 4, 15, "X")], ["A", "B", "c", "j"])

    parameters = {
        "options": {
            "compare_mode": "join",
            "join_keys": ["J"],
            "ignore": ["C"]
        }
    }
    options = control_and_setup(parameters, controls)["options"]

    compare_engine = CompareEngineSpark(df_source, df_expected, options)
    assert compare_engine.compare()
    assert compare_engine.error_type is None

def test_data_missmatch(spark, controls):
    df_source = spark.createDataFrame([(1, 4, "X"), (2, 5, "Y"), (3, 6, "Z")], ["A", "B", "J"])
    df_expected = spark.createDataFrame([(3, 7, "Z"), (2, 5, "Y"), (1, 4, "X")], ["A", "B", "J"])

    parameters = {
        "options": {
            "compare_mode": "join",
            "join_keys": ["J"]
        }
    }
    options = control_and_setup(parameters, controls)["options"]

    compare_engine = CompareEngineSpark(df_source, df_expected, options)
    assert not compare_engine.compare()
    assert compare_engine.error_type == "data"

def test_data_missmatch_ignore(spark, controls):
    df_source = spark.createDataFrame([(1, 4, "X"), (2, 5, "Y"), (3, 6, "Z")], ["A", "B", "J"])
    df_expected = spark.createDataFrame([(3, 7, "Z"), (2, 5, "Y"), (1, 4, "X")], ["A", "B", "J"])

    parameters = {
        "options": {
            "compare_mode": "join",
            "join_keys": ["J"],
            "ignore": ["B"]
        }
    }
    options = control_and_setup(parameters, controls)["options"]

    compare_engine = CompareEngineSpark(df_source, df_expected, options)
    assert compare_engine.compare()
    assert compare_engine.error_type is None

def test_data_case_insensitive(spark, controls):
    df_source = spark.createDataFrame([("a", "b", "X"), ("c", "d", "Y"), ("e", "f", "Z")], ["A", "B", "J"])
    df_expected = spark.createDataFrame([("e", "f", "Z"), ("C", "D", "Y"), ("A", "B", "X")], ["A", "B", "J"])

    parameters = {
        "options": {
            "compare_mode": "join",
            "join_keys": ["J"],
            "case_insensitive": True
        }
    }
    options = control_and_setup(parameters, controls)["options"]

    compare_engine = CompareEngineSpark(df_source, df_expected, options)
    assert compare_engine.compare()
    assert compare_engine.error_type is None

def test_data_case_sensitive_failure(spark, controls):
    df_source = spark.createDataFrame([("a", "b", "X"), ("c", "d", "Y"), ("e", "f", "Z")], ["A", "B", "J"])
    df_expected = spark.createDataFrame([("e", "f", "Z"), ("C", "D", "Y"), ("A", "B", "X")], ["A", "B", "J"])

    parameters = {
        "options": {
            "compare_mode": "join",
            "join_keys": ["J"],
            "case_insensitive": False
        }
    }
    options = control_and_setup(parameters, controls)["options"]

    compare_engine = CompareEngineSpark(df_source, df_expected, options)
    assert not compare_engine.compare()
    assert compare_engine.error_type == "data"

def test_data_trim(spark, controls):
    df_source = spark.createDataFrame([(" a", "b ", "x "), ("c ", " d", "y"), ("e", " f ", "z")], ["A", "B", "J"])
    df_expected = spark.createDataFrame([("e", "f", "z"), ("c", "d", "y"), ("a", "b", "x")], ["A", "B", "J"])

    parameters = {
        "options": {
            "compare_mode": "join",
            "join_keys": ["J"],
            "trim": True
        }
    }
    options = control_and_setup(parameters, controls)["options"]

    compare_engine = CompareEngineSpark(df_source, df_expected, options)
    assert compare_engine.compare()
    assert compare_engine.error_type is None

def test_data_trim_failure(spark, controls):
    df_source = spark.createDataFrame([(" a", "b ", "x "), ("c ", " d", "y"), ("e", "f ", "z")], ["A", "B", "J"])
    df_expected = spark.createDataFrame([("e", "f", "z"), ("c", "d", "y"), ("a", "b", "x")], ["A", "B", "J"])

    parameters = {
        "options": {
            "compare_mode": "join",
            "join_keys": ["J"],
            "trim": False
        }
    }
    options = control_and_setup(parameters, controls)["options"]

    compare_engine = CompareEngineSpark(df_source, df_expected, options)
    assert not compare_engine.compare()
    assert compare_engine.error_type == "data"

def test_data_tolerance(spark, controls):
    df_source = spark.createDataFrame([(0, 4, "X"), (4, 5, "Y"), (5, 6, "Z")], ["A", "B", "J"])
    df_expected = spark.createDataFrame([(3, 6, "Z"), (2, 5, "Y"), (1, 4, "X")], ["A", "B", "J"])

    parameters = {
        "options": {
            "compare_mode": "join",
            "join_keys": ["J"],
            "tolerance": 2
        }
    }
    options = control_and_setup(parameters, controls)["options"]

    compare_engine = CompareEngineSpark(df_source, df_expected, options)
    assert compare_engine.compare()
    assert compare_engine.error_type is None

def test_data_tolerance_failure(spark, controls):
    df_source = spark.createDataFrame([(0, 4, "X"), (4, 5, "Y"), (5, 6, "Z")], ["A", "B", "J"])
    df_expected = spark.createDataFrame([(3, 6, "Z"), (2, 5, "Y"), (1, 4, "X")], ["A", "B", "J"])

    parameters = {
        "options": {
            "compare_mode": "join",
            "join_keys": ["J"]
        }
    }
    options = control_and_setup(parameters, controls)["options"]

    compare_engine = CompareEngineSpark(df_source, df_expected, options)
    assert not compare_engine.compare()
    assert compare_engine.error_type == "data"
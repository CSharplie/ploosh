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
        .master("local[*]") \
        .config("spark.executor.memory", "1g") \
        .config("spark.driver.memory", "1g") \
        .getOrCreate()

def test_success(spark, controls):
    df_source = spark.createDataFrame([(1, 4), (2, 5), (3, 6)], ["A", "B"])
    df_expected = spark.createDataFrame([(1, 4), (2, 5), (3, 6)], ["A", "B"])
    parameters = {}
    options = control_and_setup(parameters, controls)["options"]

    compare_engine = CompareEngineSpark(df_source, df_expected, options)
    assert compare_engine.compare()
    assert compare_engine.error_type is None

def test_mismatches_headers(spark, controls):
    df_source = spark.createDataFrame([(1, 4), (2, 5), (3, 6)], ["A", "B"])
    df_expected = spark.createDataFrame([(1, 4), (2, 5), (3, 6)], ["A", "C"])

    parameters = {}
    options = control_and_setup(parameters, controls)["options"]

    compare_engine = CompareEngineSpark(df_source, df_expected, options)
    assert not compare_engine.compare()
    assert compare_engine.error_type == "headers"

def test_header_case_insensitive(spark, controls):
    df_source = spark.createDataFrame([(1, 4), (2, 5), (3, 6)], ["A", "B"])
    df_expected = spark.createDataFrame([(1, 4), (2, 5), (3, 6)], ["a", "b"])

    parameters = {}
    options = control_and_setup(parameters, controls)["options"]

    compare_engine = CompareEngineSpark(df_source, df_expected, options)
    assert compare_engine.compare()
    assert compare_engine.error_type is None

def test_header_ignore(spark, controls):
    df_source = spark.createDataFrame([(1, 4), (2, 5), (3, 6)], ["A", "B"])
    df_expected = spark.createDataFrame([(1, 4), (2, 5), (3, 6)], ["A", "C"])

    parameters = {
        "options": {
            "ignore": ["C"]
        }
    }
    options = control_and_setup(parameters, controls)["options"]

    compare_engine = CompareEngineSpark(df_source, df_expected, options)
    assert compare_engine.compare()
    assert compare_engine.error_type is None

def test_column_sort(spark, controls):
    df_source = spark.createDataFrame([(1, 4), (2, 5), (3, 6)], ["A", "B"])
    df_expected = spark.createDataFrame([(4, 1), (5, 2), (6, 3)], ["B", "A"])

    parameters = {}
    options = control_and_setup(parameters, controls)["options"]

    compare_engine = CompareEngineSpark(df_source, df_expected, options)
    assert compare_engine.compare()

def test_count_failure(spark, controls):
    df_source = spark.createDataFrame([(1, 4), (2, 5), (3, 6)], ["A", "B"])
    df_expected = spark.createDataFrame([(1, 4), (2, 5)], ["A", "B"])

    parameters = {}
    options = control_and_setup(parameters, controls)["options"]

    compare_engine = CompareEngineSpark(df_source, df_expected, options)
    assert not compare_engine.compare()
    assert compare_engine.error_type == "count"

def test_data_mismatch(spark, controls):
    df_source = spark.createDataFrame([(1, 4), (2, 5), (3, 6)], ["A", "B"])
    df_expected = spark.createDataFrame([(1, 4), (2, 5), (3, 7)], ["A", "B"])

    parameters = {}
    options = control_and_setup(parameters, controls)["options"]

    compare_engine = CompareEngineSpark(df_source, df_expected, options)
    assert not compare_engine.compare()
    assert compare_engine.error_type == "data"

def test_data_mismatch_ignore(spark, controls):
    df_source = spark.createDataFrame([(1, 4), (2, 5), (3, 6)], ["A", "B"])
    df_expected = spark.createDataFrame([(1, 4), (2, 5), (3, 7)], ["A", "B"])

    parameters = {
        "options": {
            "ignore": ["B"]
        }
    }
    options = control_and_setup(parameters, controls)["options"]

    compare_engine = CompareEngineSpark(df_source, df_expected, options)
    assert compare_engine.compare()
    assert compare_engine.error_type is None

def test_data_case_insensitive(spark, controls):
    df_source = spark.createDataFrame([("TOTO", "COCO"), ("TITI", "CICI"), ("TATA", "CACA")], ["A", "B"])
    df_expected = spark.createDataFrame([("toto", "coco"), ("titi", "cici"), ("tata", "caca")], ["a", "b"])

    parameters = {
        "options": {
            "ignore": ["B"],
            "case_insensitive": True
        }
    }
    options = control_and_setup(parameters, controls)["options"]

    compare_engine = CompareEngineSpark(df_source, df_expected, options)
    assert compare_engine.compare()
    assert compare_engine.error_type is None

def test_data_case_insensitive_failure(spark, controls):
    df_source = spark.createDataFrame([("TOTO", "COCO"), ("TITI", "CICI"), ("TATA", "CACA")], ["A", "B"])
    df_expected = spark.createDataFrame([("toto", "coco"), ("titi", "cici"), ("tata", "caca")], ["a", "b"])

    parameters = {
        "options": {
            "ignore": ["B"],
            "case_insensitive": False
        }
    }
    options = control_and_setup(parameters, controls)["options"]

    compare_engine = CompareEngineSpark(df_source, df_expected, options)
    assert not compare_engine.compare()
    assert compare_engine.error_type == "data"

def test_data_trim(spark, controls):
    df_source = spark.createDataFrame([("TOTO ", "COCO"), (" TITI", "CICI "), (" TATA ", "CACA")], ["A", "B"])
    df_expected = spark.createDataFrame([("TOTO", "COCO"), ("TITI", "CICI"), ("TATA", "CACA")], ["A", "B"])

    parameters = {
        "options": {
            "trim": True
        }
    }
    options = control_and_setup(parameters, controls)["options"]

    compare_engine = CompareEngineSpark(df_source, df_expected, options)
    assert compare_engine.compare()
    assert compare_engine.error_type is None

def test_data_trim_failure(spark, controls):
    df_source = spark.createDataFrame([("TOTO ", "COCO"), (" TITI", "CICI "), (" TATA ", "CACA")], ["A", "B"])
    df_expected = spark.createDataFrame([("TOTO", "COCO"), ("TITI", "CICI"), ("TATA", "CACA")], ["A", "B"])

    parameters = {
        "options": {
            "trim": False
        }
    }
    options = control_and_setup(parameters, controls)["options"]

    compare_engine = CompareEngineSpark(df_source, df_expected, options)
    assert not compare_engine.compare()
    assert compare_engine.error_type == "data"

def test_data_tolerance(spark, controls):
    df_source = spark.createDataFrame([(1.0, 4.0), (2.0, 5.0), (3.0, 6.0)], ["A", "B"])
    df_expected = spark.createDataFrame([(1.0, 4.0), (2.0, 5.0), (3.0, 6.1)], ["A", "B"])

    parameters = {
        "options": {
            "tolerance": 0.1
        }
    }
    options = control_and_setup(parameters, controls)["options"]

    compare_engine = CompareEngineSpark(df_source, df_expected, options)
    assert compare_engine.compare()
    assert compare_engine.error_type is None

def test_data_tolerance_failure(spark, controls):
    df_source = spark.createDataFrame([(1.0, 4.0), (2.0, 5.0), (3.0, 6.0)], ["A", "B"])
    df_expected = spark.createDataFrame([(1.0, 4.0), (2.0, 5.0), (3.0, 6.1)], ["A", "B"])

    parameters = {
        "options": {
            "tolerance": 0.01
        }
    }
    options = control_and_setup(parameters, controls)["options"]

    compare_engine = CompareEngineSpark(df_source, df_expected, options)
    assert not compare_engine.compare()
    assert compare_engine.error_type == "data"

def test_data_sort(spark, controls):
    df_source = spark.createDataFrame([(1, 4), (2, 5), (3, 6)], ["A", "B"])
    df_expected = spark.createDataFrame([(3, 6), (2, 5), (1, 4)], ["A", "B"])

    parameters = {
        "options": {
            "sort": ["A"]
        }
    }
    options = control_and_setup(parameters, controls)["options"]

    compare_engine = CompareEngineSpark(df_source, df_expected, options)
    assert compare_engine.compare()
    assert compare_engine.error_type is None

def test_empty_dataframes(spark, controls):
    schema = StructType([
        StructField("A", IntegerType(), True),
        StructField("B", IntegerType(), True),
    ])

    df_source = spark.createDataFrame([], schema)
    df_expected = spark.createDataFrame([], schema)

    parameters = {}
    options = control_and_setup(parameters, controls)["options"]

    compare_engine = CompareEngineSpark(df_source, df_expected, options)
    assert compare_engine.compare()
    assert compare_engine.error_type is None
    
def test_empty_dataframes_failure(spark, controls):
    schema = StructType([
        StructField("A", IntegerType(), True),
        StructField("B", IntegerType(), True),
    ])

    df_source = spark.createDataFrame([], schema)
    df_expected = spark.createDataFrame([(1, 4), (2, 5), (3, 6)], ["A", "B"])

    parameters = {
        "options": {
            "allow_no_rows": False
        }
    }
    options = control_and_setup(parameters, controls)["options"]

    compare_engine = CompareEngineSpark(df_source, df_expected, options)
    assert not compare_engine.compare()
    assert compare_engine.error_type == "count"

def test_empty_dataframes_asymmetric(spark, controls):
    schema = StructType([
        StructField("A", IntegerType(), True),
        StructField("B", IntegerType(), True),
    ])

    df_source = spark.createDataFrame([], schema)
    df_expected = spark.createDataFrame([], StructType([]))

    parameters = {}
    options = control_and_setup(parameters, controls)["options"]

    compare_engine = CompareEngineSpark(df_source, df_expected, options)
    assert compare_engine.compare()
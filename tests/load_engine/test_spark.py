from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, TimestampType, FloatType
import pytest
from pyjeb import control_and_setup
from ploosh.engines.load_engine_spark import LoadEngineSpark
from ploosh.configuration import Configuration

@pytest.fixture
def controls():
    controls = Configuration.case_definition
    controls = [control for control in controls if control["name"].startswith("options")]
    return controls


@pytest.fixture
def spark():
    return SparkSession.builder \
        .appName("CSV_to_Table") \
        .master("spark://localhost:7077") \
        .config("spark.executor.memory", "1g") \
        .config("spark.driver.memory", "1g") \
        .getOrCreate()

def test_count(spark, controls):
    schema = StructType([
        StructField("A", IntegerType(), True),
        StructField("B", IntegerType(), True)
    ])
    df_data = spark.createDataFrame([(1, 4), (2, 5), (3, 6)], schema)
    parameters = {}
    options = control_and_setup(parameters, controls)["options"]

    load_engine = LoadEngineSpark(None, options, None)
    df_data = load_engine.execute(df_data)
    assert load_engine.count == 3

def test_cast_datetime(spark, controls):
    schema = StructType([
        StructField("A", IntegerType(), True),
        StructField("B", StringType(), True)
    ])
    df_data = spark.createDataFrame([(1, "2021-01-01"), (2, "2021-01-01"), (3, "2021-01-01")], schema)
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

    load_engine = LoadEngineSpark(None, options, None)
    df_data = load_engine.execute(df_data)

    assert df_data.schema["B"].dataType == TimestampType()
    assert df_data.schema["A"].dataType == IntegerType()

def test_cast_int(spark, controls):
    schema = StructType([
        StructField("A", IntegerType(), True),
        StructField("B", StringType(), True)
    ])
    df_data = spark.createDataFrame([(1, "4"), (2, "5"), (3, "6")], schema)
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

    load_engine = LoadEngineSpark(None, options, None)
    df_data = load_engine.execute(df_data)

    assert df_data.schema["B"].dataType == IntegerType()
    assert df_data.schema["A"].dataType == IntegerType()

def test_cast_float(spark, controls):
    schema = StructType([
        StructField("A", IntegerType(), True),
        StructField("B", StringType(), True)
    ])
    df_data = spark.createDataFrame([(1, "4.0"), (2, "5.0"), (3, "6.0")], schema)
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

    load_engine = LoadEngineSpark(None, options, None)
    df_data = load_engine.execute(df_data)

    assert df_data.schema["B"].dataType == FloatType()
    assert df_data.schema["A"].dataType == IntegerType()
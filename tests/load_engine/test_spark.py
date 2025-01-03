from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType
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
# Local Spark setup

You can run Ploosh with a local Spark session for development and testing.

## Prerequisites

- Python 3.8+
- PySpark installed: `pip install pyspark`
- Ploosh installed: `pip install ploosh`

## Usage

``` python
from pyspark.sql import SparkSession
from ploosh import execute_cases

# Initialize a local Spark session
spark = SparkSession.builder \
    .appName("Ploosh") \
    .master("local[*]") \
    .getOrCreate()

# Execute test cases
execute_cases(
    cases="test_cases",
    connections="connections.yml",
    spark_session=spark
)
```

## When to use local Spark

- **Developing and debugging** Spark test cases before deploying to Fabric or Databricks
- **Testing Spark-specific features** like join mode comparison or Spark SQL queries
- **Working with local files** (CSV, JSON, Parquet, Delta) that you want to test with the Spark engine

## Example test case

``` yaml
Test local delta:
  source:
    type: delta_spark
    path: ./data/employees_delta
  expected:
    type: csv_spark
    path: ./data/expected_employees.csv
    header: true
    inferSchema: true
```

## Command line

You can also use Spark mode from the command line:

``` shell
ploosh --cases test_cases --connections connections.yml --spark true
```

When `--spark true` is set and no `spark_session` is provided, Ploosh automatically creates a local SparkSession.

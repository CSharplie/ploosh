# Parquet (Spark)

This connector is used to read Parquet files using Spark.

> ⚠️ A Spark connector can only be used with another Spark connector. It is not possible to mix Spark and native connectors in the same test case.

See [Spark mode overview](/docs/spark/overview) for more information.

## Connection configuration

No connection is required by this connector.

## Test case configuration

| Name | Mandatory | Default | Description |
|------|:---------:|:-------:|-------------|
| path | yes | | Path to the Parquet file |

### Example

``` yaml
Example Parquet Spark:
  source:
    type: parquet_spark
    path: /lakehouse/default/Files/data/employees.parquet
  expected:
    type: sql_spark
    query: |
      SELECT *
      FROM expected_employees
```

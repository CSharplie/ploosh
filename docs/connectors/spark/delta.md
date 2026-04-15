# Delta (Spark)

This connector is used to read Delta tables using Spark.

> ⚠️ A Spark connector can only be used with another Spark connector. It is not possible to mix Spark and native connectors in the same test case.

See [Spark mode overview](/docs/spark/overview) for more information.

## Connection configuration

No connection is required by this connector.

## Test case configuration

| Name | Mandatory | Default | Description |
|------|:---------:|:-------:|-------------|
| path | yes | | Path to the Delta table directory |

### Example

``` yaml
Example Delta Spark:
  source:
    type: delta_spark
    path: /lakehouse/default/Tables/employees
  expected:
    type: csv_spark
    path: /lakehouse/default/Files/expected/employees.csv
    header: true
    inferSchema: true
```

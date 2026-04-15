# JSON (Spark)

This connector is used to read JSON files using Spark.

> ⚠️ A Spark connector can only be used with another Spark connector. It is not possible to mix Spark and native connectors in the same test case.

See [Spark mode overview](/docs/spark/overview) for more information.

## Connection configuration

No connection is required by this connector.

## Test case configuration

| Name | Mandatory | Default | Description |
|------|:---------:|:-------:|-------------|
| path | yes | | Path to the JSON file |
| multiline | no | `true` | Enable reading of multi-line JSON files |
| encoding | no | `UTF-8` | Encoding to use when reading the file |
| lineSep | no | `\n` | Character used to denote a line break |

### Example

``` yaml
Example JSON Spark:
  source:
    type: json_spark
    path: /lakehouse/default/Files/data/employees.json
    multiline: true
  expected:
    type: sql_spark
    query: |
      SELECT *
      FROM expected_employees
```

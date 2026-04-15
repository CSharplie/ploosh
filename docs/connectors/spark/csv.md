# CSV (Spark)

This connector is used to read CSV files using Spark.

> ⚠️ A Spark connector can only be used with another Spark connector. It is not possible to mix Spark and native connectors in the same test case.

See [Spark mode overview](/docs/spark/overview) for more information.

## Connection configuration

No connection is required by this connector.

## Test case configuration

| Name | Mandatory | Default | Description |
|------|:---------:|:-------:|-------------|
| path | yes | | Path to the CSV file (supports wildcards, e.g. `*.csv`) |
| delimiter | no | `,` | Delimiter used in the CSV file |
| header | no | `true` | Whether the CSV file has a header row |
| inferSchema | no | `false` | Automatically infer column types from data |
| multiline | no | `false` | Enable parsing of records spanning multiple lines |
| quote | no | `"` | Character used to denote the start and end of a quoted item |
| encoding | no | `UTF-8` | Encoding to use when reading the file |
| lineSep | no | `\n` | Character used to denote a line break |

### Example

``` yaml
Example CSV Spark:
  source:
    type: csv_spark
    path: /lakehouse/default/Files/data/employees/*.csv
    header: true
    inferSchema: true
  expected:
    type: sql_spark
    query: |
      SELECT *
      FROM expected_employees
```

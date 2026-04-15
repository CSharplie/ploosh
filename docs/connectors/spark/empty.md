# Empty (Spark)

This connector returns an empty Spark DataFrame (0 rows, 0 columns). It is used as the expected side of a test case when the source query should return no data.

> ⚠️ A Spark connector can only be used with another Spark connector. It is not possible to mix Spark and native connectors in the same test case.

See [Spark mode overview](/docs/spark/overview) for more information.

## Connection configuration

No connection is required by this connector.

## Test case configuration

No configuration is required by this connector.

### Example

``` yaml
Test no anomalies:
  source:
    type: sql_spark
    query: |
      SELECT *
      FROM lakehouse.fact_orders
      WHERE amount < 0
  expected:
    type: empty_spark
```

## Use cases

- Verify absence of anomalies or invalid data in Lakehouse tables
- Check for duplicates in distributed datasets
- Validate KQL query returns no critical events

See [Testing approaches](/docs/use-cases/testing-approaches) for more examples.

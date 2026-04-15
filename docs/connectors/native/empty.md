# Empty

This connector returns an empty DataFrame (0 rows, 0 columns). It is used as the expected side of a test case when the source query should return no data.

## Connection configuration

No connection is required by this connector.

## Test case configuration

No configuration is required by this connector.

### Example

``` yaml
Test no invalid records:
  source:
    connection: my_database
    type: mssql
    query: |
      SELECT *
      FROM fact_orders
      WHERE amount < 0
  expected:
    type: empty
```

## Use cases

- Verify absence of anomalies or invalid data
- Check for duplicates
- Validate referential integrity
- Ensure no NULL values in mandatory columns

See [Testing approaches](/docs/use-cases/testing-approaches) for more examples.

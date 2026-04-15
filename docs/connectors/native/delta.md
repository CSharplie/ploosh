# Delta

This connector is used to read local Delta tables using the `deltalake` library.

## Connection configuration

No connection is required by this connector.

## Test case configuration

| Name | Mandatory | Default | Description |
|------|:---------:|:-------:|-------------|
| path | yes | | Path to the Delta table directory |

### Example

``` yaml
Example Delta:
  source:
    type: delta
    path: ./data/employees_delta
  expected:
    type: csv
    path: ./data/expected_employees.csv
```

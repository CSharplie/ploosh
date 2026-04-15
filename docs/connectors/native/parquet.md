# Parquet

This connector is used to read local Parquet files.

## Connection configuration

No connection is required by this connector.

## Test case configuration

| Name | Mandatory | Default | Description |
|------|:---------:|:-------:|-------------|
| path | yes | | Path to the Parquet file |
| columns | no | | List of columns to load (subset) |
| engine | no | `auto` | Parquet engine: `auto`, `pyarrow`, or `fastparquet` |
| filters | no | | List of row group filters to apply |
| filters.column | yes | | Column name to filter on |
| filters.operator | yes | | Comparison operator: `==`, `=`, `>`, `>=`, `<`, `<=`, `!=` |
| filters.value | yes | | Value to filter by |

### Example

``` yaml
Example Parquet:
  source:
    type: parquet
    path: ./data/employees.parquet
  expected:
    type: csv
    path: ./data/expected_employees.csv
```

### Example with column selection

``` yaml
Example Parquet with columns:
  source:
    type: parquet
    path: ./data/employees.parquet
    columns:
      - id
      - name
      - department
  expected:
    type: empty
```

### Example with filters

``` yaml
Example Parquet with filters:
  source:
    type: parquet
    path: ./data/employees.parquet
    filters:
      - column: department_id
        operator: "=="
        value: 5
  expected:
    type: csv
    path: ./data/expected_dept5.csv
```

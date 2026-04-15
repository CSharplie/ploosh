# Databricks

This connector is used to query a Databricks SQL warehouse or cluster using SQL.

## Connection configuration

| Name | Mandatory | Default | Description |
|------|:---------:|:-------:|-------------|
| token | yes | | Personal Access Token (PAT) for authentication |
| hostname | yes | | Databricks instance hostname (e.g. `adb-1234567890.1.azuredatabricks.net`) |
| database | yes | | Database name |
| http_path | yes | | HTTP path for the SQL warehouse or cluster (found in JDBC/ODBC settings) |
| port | no | `443` | Port number |

### Example

``` yaml
connections:
  databricks_connection:
    type: databricks
    token: $var.databricks_token
    hostname: adb-1234567890.1.azuredatabricks.net
    database: my_database
    http_path: /sql/1.0/warehouses/abc123
```

## Test case configuration

| Name | Mandatory | Default | Description |
|------|:---------:|:-------:|-------------|
| query | yes | | SQL query to execute |

### Example

``` yaml
Example Databricks:
  source:
    type: databricks
    connection: databricks_connection
    query: |
      SELECT *
      FROM employees
      WHERE hire_date < '2000-01-01'
  expected:
    type: csv
    path: data/employees_before_2000.csv
```

## Requirements

- `pip install databricks-sqlalchemy` (included in `ploosh` full installation)

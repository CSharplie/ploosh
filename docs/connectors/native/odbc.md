# ODBC

This connector is used to query any database accessible via an ODBC driver.

## Connection configuration

Two connection modes are available: `DSN` and `connection_string`.

### DSN mode

| Name | Mandatory | Default | Description |
|------|:---------:|:-------:|-------------|
| mode | no | `DSN` | Connection mode: `DSN` or `connection_string` |
| DSN | yes | | Data Source Name configured on the system |
| auto_commit | no | `true` | Enable auto-commit |
| use_credentials | no | `false` | Whether to pass username/password |
| user | no | | Username (when `use_credentials` is `true`) |
| password | no | | Password (when `use_credentials` is `true`) |
| encoding | no | `UTF-8` | Encoding for the connection |

### Connection string mode

| Name | Mandatory | Default | Description |
|------|:---------:|:-------:|-------------|
| mode | yes | | Must be `connection_string` |
| connection_string | yes | | ODBC connection string |
| auto_commit | no | `true` | Enable auto-commit |
| encoding | no | `UTF-8` | Encoding for the connection |

### Example (DSN mode)

``` yaml
connections:
  odbc_connection:
    type: odbc
    DSN: my_data_source
    use_credentials: true
    user: my_user
    password: $var.odbc_password
```

### Example (connection string mode)

``` yaml
connections:
  odbc_connection:
    type: odbc
    mode: connection_string
    connection_string: "Driver={ODBC Driver 18 for SQL Server};Server=myserver;Database=mydb;Uid=myuser;Pwd=mypassword;"
```

## Test case configuration

| Name | Mandatory | Default | Description |
|------|:---------:|:-------:|-------------|
| query | yes | | SQL query to execute |

### Example

``` yaml
Example ODBC:
  source:
    type: odbc
    connection: odbc_connection
    query: |
      SELECT *
      FROM employees
      WHERE department = 'Engineering'
  expected:
    type: csv
    path: data/expected_engineers.csv
```

## Requirements

- `pip install pyodbc` (included in `ploosh` full installation)
- An ODBC driver installed and a DSN configured on the system

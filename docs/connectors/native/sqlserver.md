# SQL Server

This connector is used to query a Microsoft SQL Server database using SQL.

> **Requirement**: ODBC Driver 18 for SQL Server must be installed on the system.
>
> Installation guides: [Windows](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server) | [Linux](https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server) | [macOS](https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/install-microsoft-odbc-driver-sql-server-macos)

## Connection configuration

Two connection modes are available: `password` and `connection_string`.

### Password mode

| Name | Mandatory | Default | Description |
|------|:---------:|:-------:|-------------|
| mode | no | `password` | Connection mode: `password` or `connection_string` |
| hostname | yes | | Server hostname or IP address |
| database | yes | | Database name |
| username | yes | | Username |
| password | yes | | Password |
| port | no | `1433` | Port number |
| encrypt | no | `true` | Enable connection encryption |
| trust_server_certificate | no | `false` | Trust the server certificate without validation |
| driver | no | `ODBC Driver 18 for SQL Server` | ODBC driver name |

### Connection string mode

| Name | Mandatory | Default | Description |
|------|:---------:|:-------:|-------------|
| mode | yes | | Must be `connection_string` |
| connection_string | yes | | SQLAlchemy connection string |

### Example (password mode)

``` yaml
connections:
  mssql_connection:
    type: mssql
    hostname: my-server.database.windows.net
    database: my_database
    username: my_user
    password: $var.mssql_password
    port: 1433
    encrypt: true
    trust_server_certificate: false
```

### Example (connection string mode)

``` yaml
connections:
  mssql_connection:
    type: mssql
    mode: connection_string
    connection_string: mssql+pyodbc:///?odbc_connect=Driver={ODBC Driver 18 for SQL Server};Server=myserver;Database=mydb;Uid=myuser;Pwd=mypassword;Encrypt=yes;
```

## Test case configuration

| Name | Mandatory | Default | Description |
|------|:---------:|:-------:|-------------|
| query | yes | | SQL query to execute |

### Example

``` yaml
Example SQL Server:
  source:
    type: mssql
    connection: mssql_connection
    query: |
      SELECT *
      FROM employees
      WHERE hire_date < '2000-01-01'
  expected:
    type: csv
    path: data/employees_before_2000.csv
```

## Requirements

- [ODBC Driver 18 for SQL Server](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)
- `pip install pyodbc` (included in `ploosh` full installation)

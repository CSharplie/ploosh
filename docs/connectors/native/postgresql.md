# PostgreSQL

This connector is used to query a PostgreSQL database using SQL.

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
| port | no | `5432` | Port number |
| ssl_context | no | `false` | Enable SSL connection |

### Connection string mode

| Name | Mandatory | Default | Description |
|------|:---------:|:-------:|-------------|
| mode | yes | | Must be `connection_string` |
| connection_string | yes | | SQLAlchemy connection string |

### Example (password mode)

``` yaml
connections:
  postgresql_connection:
    type: postgresql
    hostname: my-server.postgres.database.azure.com
    database: my_database
    username: my_user
    password: $var.pg_password
    port: 5432
    ssl_context: true
```

### Example (connection string mode)

``` yaml
connections:
  postgresql_connection:
    type: postgresql
    mode: connection_string
    connection_string: postgresql+pg8000://user:password@host:5432/database
```

## Test case configuration

| Name | Mandatory | Default | Description |
|------|:---------:|:-------:|-------------|
| query | yes | | SQL query to execute |

### Example

``` yaml
Example PostgreSQL:
  source:
    type: postgresql
    connection: postgresql_connection
    query: |
      SELECT *
      FROM employees
      WHERE hire_date < '2000-01-01'
  expected:
    type: csv
    path: data/employees_before_2000.csv
```

## Requirements

- `pip install pg8000` (included in `ploosh` full installation)

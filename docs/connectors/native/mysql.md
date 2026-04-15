# MySQL

This connector is used to query a MySQL database using SQL.

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
| port | no | `3306` | Port number |
| require_secure_transport | no | `false` | Enable SSL/TLS transport |

### Connection string mode

| Name | Mandatory | Default | Description |
|------|:---------:|:-------:|-------------|
| mode | yes | | Must be `connection_string` |
| connection_string | yes | | SQLAlchemy connection string |

### Example (password mode)

``` yaml
connections:
  mysql_connection:
    type: mysql
    hostname: my-server.database.windows.net
    database: my_database
    username: my_user
    password: $var.mysql_password
    port: 3306
```

### Example (connection string mode)

``` yaml
connections:
  mysql_connection:
    type: mysql
    mode: connection_string
    connection_string: mysql+pymysql://user:password@host:3306/database
```

## Test case configuration

| Name | Mandatory | Default | Description |
|------|:---------:|:-------:|-------------|
| query | yes | | SQL query to execute |

### Example

``` yaml
Example MySQL:
  source:
    type: mysql
    connection: mysql_connection
    query: |
      SELECT *
      FROM employees
      WHERE hire_date < '2000-01-01'
  expected:
    type: csv
    path: data/employees_before_2000.csv
```

## Requirements

- `pip install pymysql` (included in `ploosh` full installation)

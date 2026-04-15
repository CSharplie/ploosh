# Snowflake

This connector is used to query a Snowflake data warehouse using SQL.

## Connection configuration

| Name | Mandatory | Default | Description |
|------|:---------:|:-------:|-------------|
| account_identifier | yes | | Snowflake account identifier (e.g. `xy12345.us-east-1`) |
| username | yes | | Username |
| password | yes | | Password |
| database | no | | Database name |
| schema | no | | Schema name |
| warehouse | no | | Warehouse name |
| role | no | | Role name |

### Example

``` yaml
connections:
  snowflake_connection:
    type: snowflake
    account_identifier: xy12345.us-east-1
    username: my_user
    password: $var.snowflake_password
    database: my_database
    schema: public
    warehouse: my_warehouse
    role: my_role
```

## Test case configuration

| Name | Mandatory | Default | Description |
|------|:---------:|:-------:|-------------|
| query | yes | | SQL query to execute |

### Example

``` yaml
Example Snowflake:
  source:
    type: snowflake
    connection: snowflake_connection
    query: |
      SELECT *
      FROM employees
      WHERE hire_date < '2000-01-01'
  expected:
    type: csv
    path: data/employees_before_2000.csv
```

## Requirements

- `pip install snowflake-sqlalchemy` (included in `ploosh` full installation)

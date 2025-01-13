This connector allows to connect to a ODBC datasource and execute SQL queries.

# Connection configuration
## Definition
| Name                     | Mandatory | Default    | Description |
|--------------------------|:---------:|:----------:|-------------|
| dsn                      | yes       |            | Data Source Name
| auto_commit              | no        | true       | Autocommit mode
| username                 | no        | null       | User name
| password                 | no        | null       | User password
| driver                   | no        | null       | ODBC driver name
| encoding                 | no        | UTF-8      | Encoding to use for the connection

:warning: it's highly recommended to use a [parameter](/docs/configuration-custom-parameters/) to pass the password value

## Example
``` yaml
odbc_example:
  type: odbc
  dsn: my_dsn
  username: pixel
  password: $var.odbc_password
```

# Test case configuration
## Definition
| Name              | Mandatory | Default                       | Description |
|-------------------|:---------:|:-----------------------------:|-------------|
| connection        | yes       |                               | The connection to use
| query             | yes       |                               | The query to execute to the database

## Example
``` yaml
Example ODBC:
  source:
    connection: odbc_example
    type: odbc
    query: | 
        select * 
            from employees
            where hire_date < '2000-01-01'
    type: csv
    path: data/employees_before_2000.csv
```
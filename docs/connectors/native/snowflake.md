This connector allows to connect to a Snowflake instance and execute SQL queries.

# Connection configuration
## Definition
| Name                     | Mandatory | Default    | Description |
|--------------------------|:---------:|:----------:|-------------|
| account_identifier       | yes       |            | Account identifier of snowflake instance
| username                 | yes       |            | User name
| password                 | yes       |            | User password
| database                 | no        | null       | Target database name
| schema                   | no        | null       | Target schema name
| warehouse                | no        | null       | Target warehouse name
| role                     | no        | null       | Target role name

⚠️ it's highly recommended to use a [parameter](/docs/configuration-custom-parameters/) to pass the password value

## Example
``` yaml
snowflake_example:
  type: snowflake
  account_identifier: bjpwtqg-kt67582
  schema: PUBLIC
  warehouse: SF_TUTS_WH
  database: SF_TUTS
  username: pixel
  password: $var.snowflake_password_db
```

# Test case configuration
## Definition
| Name              | Mandatory | Default                       | Description |
|-------------------|:---------:|:-----------------------------:|-------------|
| connection        | yes       |                               | The connection to use 
| query             | yes       |                               | The query to execute to the database

## Example
``` yaml
Example Snowflake:
  source:
    connection: snowflake_example
    type: snowflake
    query: | 
        select * 
            from RH.employees
            where hire_date < '2000-01-01'
  expected:
    type: csv
    path: data/employees_before_2000.csv
```
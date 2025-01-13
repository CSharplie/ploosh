This connector allows to connect to a PostgreSQL database and execute SQL queries.

# Connection configuration
## Password mode
### Definition
| Name          | Mandatory | Default    | Description |
|---------------|:---------:|:----------:|-------------|
| mode          | no        |  password  | Change the connection mode. Can be "password" or "connection_string". "connection_string" mode allow to use a custom connection string.
| hostname      | yes       |            | Target host name
| database      | yes       |            | Target database name
| username      | yes       |            | User name
| password      | yes       |            | User password
| port          | no        | 3306       | Port to use by the connection
| ssl_context   | No        | False      | Set True if the server require a secure transport

:warning: it's highly recommended to use a [parameter](/docs/configuration-custom-parameters/) to pass the password value

### Example
``` yaml
postgresql_example:
  type: postgresql
  hostname: ploosh.postgresql.database.azure.com
  database: SampleDB
  username: sa_ploosh
  password: $var.sa_ploosh_password 
  ssl_context: true
```

### Definition
## Connection string mode
| Name              | Mandatory | Default                       | Description |
|-------------------|:---------:|:-----------------------------:|-------------|
| mode              | no        |  password                     | Use "connection_string" value to use custom connection_string
| connection_string | yes       |                               | Connection string use to access in the database. Refer to [SQLAlchemy documentation](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html) to get the accepted format

### Example
``` yaml
postgresql_example:
  type: postgresql
  mode: connection_string
  connection_string: "postgresql+pg8000://sa_ploosh:$var.sa_ploosh_password@ploosh.postgresql.database.azure.com/SampleDB"
```

# Test case configuration
## Definition
| Name              | Mandatory | Default                       | Description |
|-------------------|:---------:|:-----------------------------:|-------------|
| connection        | yes       |                               | The connection to use 
| query             | yes       |                               | The query to execute to the database

## Example
``` yaml
Example PostgreSQL:
  source:
    connection: postgresql_example
    type: postgresql
    query: | 
        select * 
            from employees
            where hire_date < "2000-01-01"
  expected:
    type: csv
    path: data/employees_before_2000.csv
```
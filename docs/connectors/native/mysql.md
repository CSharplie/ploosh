This connector allows to connect to a MySQL database and execute SQL queries.

# Connection configuration
## Password mode
### Definition
| Name                     | Mandatory | Default    | Description |
|--------------------------|:---------:|:----------:|-------------|
| mode                     | no        |  password  | Change the connection mode. Can be "password" or "connection_string". "connection_string" mode allow to use a custom connection string.
| hostname                 | yes       |            | Target host name
| database                 | yes       |            | Target database name
| username                 | yes       |            | User name
| password                 | yes       |            | User password
| port                     | no        | 3306       | Port to use by the connection
| require_secure_transport | No        | False      | Set True if the server require a secure transport

:warning: it's highly recommended to use a [parameter](/docs/configuration-custom-parameters/) to pass the password value

### Example
``` yaml
mysql_example:
  type: mysql
  hostname: ploosh.mysql.database.azure.com
  database: SampleDB
  username: sa_ploosh
  password: $var.sa_ploosh_password 
  require_secure_transport: true
```

### Definition
## Connection string mode
| Name              | Mandatory | Default                       | Description |
|-------------------|:---------:|:-----------------------------:|-------------|
| mode              | no        |  password                     | Use "connection_string" value to use custom connection_string
| connection_string | yes       |                               | Connection string use to access in the database. Refer to [SQLAlchemy documentation](https://docs.sqlalchemy.org/en/20/dialects/mysql.html) to get the accepted format

### Example
``` yaml
mysql_example:
  type: mysql
  mode: connection_string
  connection_string: "mysql+mysqldb://sa_ploosh:$var.sa_ploosh_password@ploosh.mysql.database.azure.com/SampleDB"
```

# Test case configuration
## Definition
| Name              | Mandatory | Default                       | Description |
|-------------------|:---------:|:-----------------------------:|-------------|
| connection        | yes       |                               | The connection to use 
| query             | yes       |                               | The query to execute to the database
## Example

``` yaml
Example MySQL:
  source:
    connection: mysql_example
    type: mysql
    query: | 
      select * 
          from employees
          where hire_date < "2000-01-01"
  expected:
    type: csv
    path: data/employees_before_2000.csv
```
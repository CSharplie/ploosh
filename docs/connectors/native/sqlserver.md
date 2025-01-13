This connector allows to connect to a SQL Server database and execute SQL queries.

# Requirements
ODBC Driver 18 must be installed on the executing computer.

* For Linux, follow the instructions from [Microsoft documentation](https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver15&tabs=ubuntu18-install%2Calpine17-install%2Cdebian8-install%2Credhat7-13-install%2Crhel7-offline#18)
* For Windows, follow the instructions from [Microsoft documentation](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver15)
* For macOS, follow the instructions from [Microsoft documentation](https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/install-microsoft-odbc-driver-sql-server-macos?view=sql-server-ver15)

# Connection configuration
## Password mode
### Definition
| Name                       | Mandatory | Default                       | Description |
|----------------------------|:---------:|:-----------------------------:|-------------|
| mode                       | no        |  password                     | Change the connection mode. Can be "password" or "connection_string". "connection_string" mode allow to use a custom connection string.
| hostname                   | yes       |                               | Target host name
| database                   | yes       |                               | Target database name
| username                   | yes       |                               | Sql user name
| password                   | yes       |                               | Sql user password
| port                       | no        | 1433                          | Port to use by the connection
| trust_server_certificate   | no        | false                         | Trust the server ssl connection
| encrypt                    | no        | yes                           | Encrypt the connection
| driver                     | no        | ODBC Driver 18 for SQL Server | Driver to use by the connection

:warning: it's highly recommended to use a [parameter](/docs/configuration-custom-parameters/) to pass the password value

### Example
``` yaml
mssql_example:
  type: mssql
  hostname: ploosh.database.windows.net
  database: SampleDB
  username: sa_ploosh
  password: $var.sa_ploosh_password 
```

### Definition
## Connection string mode
| Name              | Mandatory | Default                       | Description |
|-------------------|:---------:|:-----------------------------:|-------------|
| mode              | no        |  password                     | Use "connection_string" value to use custom connection_string
| connection_string | yes       |                               | Connection string use to access in the database. Refer to [SQLAlchemy documentation](https://docs.sqlalchemy.org/en/20/dialects/mssql.html) to get the accepted format

### Example
``` yaml
mssql_example:
  type: mssql
  mode: connection_string
  connection_string: "mssql+pyodbc://ploosh01:1433/SampleDB?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes&authentication=ActiveDirectoryIntegrated"
```

# Test case configuration
## Definition
| Name              | Mandatory | Default                       | Description |
|-------------------|:---------:|:-----------------------------:|-------------|
| connection        | yes       |                               | The connection to use 
| query             | yes       |                               | The query to execute to the database

## Example
``` yaml
Example SQL Server:
  source:
    connection: mssql_example
    type: mssql
    query: | 
        select * 
            from [rh].[employees]
            where [hire_date] < '2000-01-01'
  expected:
    type: csv
    path: data/employees_before_2000.csv
```
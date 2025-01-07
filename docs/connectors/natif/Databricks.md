This connector allows you to connect to a Databricks instance and execute SQL queries.

# Connection configuration
## Definition
| Name                     | Mandatory | Default    | Description |
|--------------------------|:---------:|:----------:|-------------|
| token                    | yes       |            | a token generated from databricks. See the [documentation](https://docs.databricks.com/en/dev-tools/auth/pat.html)
| hostname                 | yes       |            | url to databricks
| database                 | yes       |            | name of the database
| http_path                | yes       |            | the value is available on [JDBC/ODBC](https://docs.databricks.com/en/integrations/compute-details.html) settings 

## Example
``` yaml
databricks_example:
  type: databricks
  hostname: adb-myproject.8.azuredatabricks.net
  database: default
  token:  $var.databricks_token
  http_path: /sql/1.0/warehouses/da000000000000000
```

# Test case configuration
## Definition
| Name              | Mandatory | Default                       | Description |
|-------------------|:---------:|:-----------------------------:|-------------|
| connection        | yes       |                               | The connection to use 
| query             | yes       |                               | The query to execute to the database


## Example
``` yaml
Example Databricks:
  source:
    connection: databricks_example
    type: databricks
    query: | 
        select * 
            from `rh.employees`
            where hire_date < "2000-01-01"
  expected:
    type: csv
    path: data/employees_before_2000.csv
```
This connector is used to execute spark SQL. 

:warning: A spark connector can be use only with another spark connector. It is not possible to use a spark connector with a non spark connector.

See [Spark documentation](Spark) for more information.

# Connection configuration
No connection is required by this connector

# Configuration
## Test case configuration
| Name              | Mandatory | Default                       | Description |
|-------------------|:---------:|:-----------------------------:|-------------|
| query             | yes       |                               | The query to execute to the database

## Example
``` yaml
Example Empty Spark:
  source:
    type: sql_spark
    query: |
      select * 
          from employees
          where hire_date < "2000-01-01"
  expected:
    type: empty_spark
```
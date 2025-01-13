This connector is used to return an empty dataframe with 0 rows and 0 columns 

:warning: A spark connector can be use only with another spark connector. It is not possible to use a spark connector with a non spark connector.

See [Spark documentation](/docs/configuration-spark-mode/) for more information.

# Connection configuration
No connection is required by this connector

# Test case configuration
## Test case configuration
Test case configuration parameter is required by this connector

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
This connector is used to return an empty dataframe with 0 rows and 0 columns 

# Connection configuration
No connection is required by this connector

# Test case configuration
## Test case configuration
Test case configuration parameter is required by this connector

## Example
``` yaml
Example Empty:
  source:
    connection: mysql_example
    type: mysql
    query: | 
        select * 
            from employees
            where hire_date < "2000-01-01"
  expected:
    type: empty
```
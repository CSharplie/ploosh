This connector is used to read Parquet files using Spark. 

:warning: A spark connector can be use only with another spark connector. It is not possible to use a spark connector with a non spark connector.

See [Spark documentation](Spark) for more information.

# Connection configuration
No connection is required by this connector

# Configuration
## Test case configuration
| Name              | Mandatory | Default                       | Description |
|-------------------|:---------:|:-----------------------------:|-------------|
| path              | yes       |                                | Path to the parquet file


## Example
``` yaml
Example Parquet Spark:
  source:
    type: parquet_spark
    path: data/employees/example.parquet

  expected:
    type: sql_spark
    query: |
      select * 
          from employees
          where hire_date < "2000-01-01"
```
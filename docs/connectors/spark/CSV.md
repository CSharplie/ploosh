This connector is used to read CSV files using Spark. 

:warning: A spark connector can be use only with another spark connector. It is not possible to use a spark connector with a non spark connector.

See [Spark documentation](Spark) for more information.

# Connection configuration
No connection is required by this connector

# Configuration
## Test case configuration
| Name              | Mandatory | Default                       | Description |
|-------------------|:---------:|:-----------------------------:|-------------|
| path              | yes       |                               | Path to the CSV
| delimiter         | no        |  ,                            | Column delimiter
| header            | no        |  true                         | Use the first row as header
| inferSchema       | no        |  False                        | Infers the input schema automatically from data
| multiline         | no        |  False                        | Parse one record, which may span multiple lines, per file
| quote             | no        |  '"'                          | Character used to denote the start and end of a quoted item
| encoding         | no        |  "UTF-8"                       | Column delimiter
| lineSep          | no        |  "\n"                          | Column delimiter


## Example
``` yaml
Example CSV Spark:
  source:
    type: csv_spark
    path: data/employees/*.csv
    multiline: False
    inferSchema: False
    encoding: "UTF-8" 
  expected:
    type: sql_spark
    query: |
      select * 
          from employees
          where hire_date < "2000-01-01"
```
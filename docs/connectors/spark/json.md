This connector is used to read JSON files using Spark. 

:warning: A spark connector can be use only with another spark connector. It is not possible to use a spark connector with a non spark connector.

See [Spark documentation](Spark) for more information.

# Connection configuration
No connection is required by this connector

# Configuration
## Test case configuration
| Name              | Mandatory | Default                       | Description |
|-------------------|:---------:|:-----------------------------:|-------------|
| path              | yes       |                                | Path to the JSON file
| multiline         | no        |  True                          | Handles multi-line JSON files
| encoding         | no         |  "UTF-8"                       | Encoding to use for UTF when reading/writing
| lineSep          | no         |  "\n"                          | Character used to denote a line break


## Example
``` yaml
Example JSON Spark:
  source:
    type: json_spark
    path: data/employees/example.JSON
    multiline: Tre
    encoding: "UTF-8"
    lineSep: "\r\n"
  expected:
    type: sql_spark
    query: |
      select * 
          from employees
          where hire_date < "2000-01-01"
```
This connector is used to read Delta files from local file system.

# Connection configuration
No connection is required by this connector

# Test case configuration
## Test case configuration
| Name              | Mandatory | Default                       | Description |
|-------------------|:---------:|:-----------------------------:|-------------|
| path              | yes       |                               | Path to the delta file 


## Example
``` yaml
Example delta:
  source:
    type: delta
    path: data/employees

  expected:
    type: csv
    infer: True
    delimiter: ";"
    encoding: "utf-8"
    engine: "python"
    path: data/employees_before_2000.csv
```
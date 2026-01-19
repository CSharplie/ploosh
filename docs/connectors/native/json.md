This connector is used to read JSON files from local file system.

# Connection configuration
No connection is required by this connector

# Test case configuration
## Test case configuration
| Name              | Mandatory | Default                       | Description |
|-------------------|:---------:|:-----------------------------:|-------------|
| path              | yes       |                               | Path to the JSON file
| lines             | no        |  False                        | Whether to treat the file as line-delimited JSON (one JSON object per line)
| nrows             | no        |  None                         | Number of rows of file to read. Useful for reading pieces of large files
| encoding          | no        |  "utf-8"                      | Encoding to use for UTF when reading/writing

## Example
``` yaml
Example JSON:
  source:
    type: json
    lines: True
    encoding: "utf-8"
    path: data/json/employees.json

  expected:
    type: csv
    infer: True
    delimiter: ";"
    encoding: "utf-8"
    engine: "python"
    path: data/employees_before_2000.csv
```
This connector is used to read Parquet files from local file system.

# Connection configuration
No connection is required by this connector

# Test case configuration
## Test case configuration
| Name              | Mandatory | Default                       | Description |
|-------------------|:---------:|:-----------------------------:|-------------|
| path              | yes       |                               | Path to the Parquet file
| columns           | no        |  None                         | Subset of columns to load
| engine            | no        |  "auto"                       | Parquet engine to use ('auto', 'pyarrow', 'fastparquet')
| filters           | no        |  None                         | Row group filters to apply (for 'pyarrow')


## Example
``` yaml
Example PARQUET:
  source:
    type: parquet
    path: ../data/parquet/source/example.parquet
    columns:  ["id", "name"]
    filters:
        - column: "id"
          operator: "!="
          value: 2


  expected:
    type: csv
    infer: True
    delimiter: ";"
    encoding: "utf-8"
    engine: "python"
    path: data/example.csv
```
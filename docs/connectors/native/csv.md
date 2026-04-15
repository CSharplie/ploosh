# CSV

This connector is used to read local CSV files.

## Connection configuration

No connection is required by this connector.

## Test case configuration

| Name | Mandatory | Default | Description |
|------|:---------:|:-------:|-------------|
| path | yes | | Path to the CSV file |
| delimiter | no | `,` | Delimiter used in the CSV file |
| infer | no | `true` | Infer column names from the first row |
| names | no | | List of column labels to apply |
| schema | no | | Dictionary of column names and types (`int`, `float`, `string`, `bool`, `datetime`) |
| usecols | no | | List of columns to select |
| skiprows | no | | Number of rows to skip at the start, or list of row indices to skip (0-indexed) |
| skipfooter | no | `0` | Number of rows to skip at the end of the file |
| nrows | no | | Number of rows to read |
| lineterminator | no | | Character used to denote a line break |
| quotechar | no | `"` | Character used to denote the start and end of a quoted item |
| encoding | no | `utf-8` | Encoding to use when reading the file |
| engine | no | | Parser engine to use (`c` or `python`) |

### Example

``` yaml
Example CSV:
  source:
    type: csv
    path: ./data/employees.csv
    delimiter: ";"
    encoding: utf-8
  expected:
    type: csv
    path: ./data/expected_employees.csv
```

### Example with schema

``` yaml
Example CSV with schema:
  source:
    type: csv
    path: ./data/employees.csv
    schema:
      id: int
      name: string
      salary: float
      hire_date: datetime
  expected:
    type: empty
```

### Example without header

``` yaml
Example CSV without header:
  source:
    type: csv
    path: ./data/no_header.csv
    infer: false
    names:
      - id
      - name
      - department
  expected:
    type: empty
```

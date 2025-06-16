This connector is used to read CSV files from local file system.

# Connection configuration
No connection is required by this connector

# Test case configuration
## Test case configuration
| Name              | Mandatory | Default                       | Description |
|-------------------|:---------:|:-----------------------------:|-------------|
| path              | yes       |                               | Path to the CSV 
| delimiter         | no        |  ,                            | Column delimiter
| infer             | no        |  True                         | Infer the column names
| names             | no        |  None                         | Sequence of column labels to apply
| usecols           | no        |  None                         | Subset of columns to select
| skiprows          | no        |  None                         | Line numbers to skip or number of lines to skip (int) at the start of the file
| skipfooter        | no        |  0                            | Number of lines at bottom of file to skip (Unsupported with engine='c')
| nrows             | no        |  None                         | Number of rows of file to read. Useful for reading pieces of large files
| lineterminator    | no        |  None                         | Character used to denote a line break
| quotechar         | no        |  '"'                          | Character used to denote the start and end of a quoted item
| encoding          | no        |  "utf-8"                      | Encoding to use for UTF when reading/writing
| engine            | no        |  None                         | Parser engine to use
| Schema            | no        |  None                         | Schema to use for the CSV file

## Example
``` yaml
Example CSV:
  source:
    connection: mysql_example
    type: mysql
    query: | 
        select * 
            from employees
            where hire_date < "2000-01-01"
  expected:
    type: csv
    infer: True
    delimiter: ";"
    encoding: "utf-8"
    engine: "python"
    path: data/employees_before_2000.csv
```

## Exemple with schema
``` yaml 
Example CSV with schema:
  source:
    connection: mysql_example
    type: mysql
    query: |
        select *
            from sales
            where sale_date < "2000-01-01"
  expected:
    type: csv
    infer: False
    delimiter: ";"
    encoding: "utf-8"
    schema:
      sale_id: string
      sale_date: datetime
      sale_amount: float
  
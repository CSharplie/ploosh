This connector is used to read Excel files from local file system.

# Connection configuration
No connection is required by this connector

# Test case configuration
# Definition

| Name      | Mandatory | Default | Description |
|-----------|:---------:|:-------:|-------------|
| path      | yes       |         | The path to the Excel file to read |
| sheet     | yes       |         | The sheet name or index to read from the Excel file

# Example

``` yaml
Example Excel:
  source:
    type: mysql
    
  expected:
    type: excel
    path: data/employees.xlsx
    sheet: employees


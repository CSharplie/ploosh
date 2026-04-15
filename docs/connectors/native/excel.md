# Excel

This connector is used to read local Excel files (.xlsx, .xls).

## Connection configuration

No connection is required by this connector.

## Test case configuration

| Name | Mandatory | Default | Description |
|------|:---------:|:-------:|-------------|
| path | yes | | Path to the Excel file |
| sheet_name | yes | | Sheet name or sheet index (0-based) |
| skiprows | no | `0` | Number of rows to skip at the start of the sheet |

### Example

``` yaml
Example Excel:
  source:
    type: excel
    path: ./data/employees.xlsx
    sheet_name: Sheet1
  expected:
    type: csv
    path: ./data/expected_employees.csv
```

### Example with sheet index

``` yaml
Example Excel by index:
  source:
    type: excel
    path: ./data/report.xlsx
    sheet_name: 0
    skiprows: 2
  expected:
    type: empty
```

## Requirements

- `openpyxl` (included in `ploosh` installation)

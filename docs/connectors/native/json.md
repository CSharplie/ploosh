# JSON

This connector is used to read local JSON files.

## Connection configuration

No connection is required by this connector.

## Test case configuration

| Name | Mandatory | Default | Description |
|------|:---------:|:-------:|-------------|
| path | yes | | Path to the JSON file |
| lines | no | `false` | Whether to treat the file as line-delimited JSON (one JSON object per line) |
| nrows | no | | Number of lines to read (line-delimited mode only) |
| encoding | no | `utf-8` | Encoding to use when reading the file |

### Example

``` yaml
Example JSON:
  source:
    type: json
    path: ./data/employees.json
  expected:
    type: csv
    path: ./data/expected_employees.csv
```

### Example with line-delimited JSON

``` yaml
Example JSONL:
  source:
    type: json
    path: ./data/events.jsonl
    lines: true
    nrows: 1000
  expected:
    type: empty
```

# CSV exporter

The CSV exporter generates a flat CSV file with one row per test case and detailed Excel files for failed tests.

## Output structure

```
{output_path}/csv/
├── test_results.csv              → Summary of all test cases
└── test_results/
    ├── Test case 1.xlsx          → Gap details (only for failed tests)
    └── Test case 2.xlsx
```

## CSV columns

| Column | Description |
|--------|-------------|
| `execution_id` | Unique identifier for the test run |
| `name` | Test case name |
| `state` | Result: `passed`, `failed`, `error`, `notExecuted` |
| `source_start` | Source data loading start time |
| `source_end` | Source data loading end time |
| `source_duration` | Source loading duration in seconds |
| `source_count` | Number of rows in source dataset |
| `source_executed_action` | Query or path executed for source |
| `expected_start` | Expected data loading start time |
| `expected_end` | Expected data loading end time |
| `expected_duration` | Expected loading duration in seconds |
| `expected_count` | Number of rows in expected dataset |
| `expected_executed_action` | Query or path executed for expected |
| `compare_start` | Comparison start time |
| `compare_end` | Comparison end time |
| `compare_duration` | Comparison duration in seconds |
| `success_rate` | Percentage of matching rows (0.0 to 1.0) |
| `error_type` | Error category: `headers`, `count`, `data`, `compare` |
| `error_message` | Error description |
| `error_detail_file_path` | Path to the XLSX gap analysis file |

## Usage

### Command line

``` shell
ploosh --connections connections.yml --cases test_cases --export CSV
```

### Python API

``` python
from ploosh import execute_cases

execute_cases(cases="test_cases", connections="connections.yml", path_output="./output")
# Then manually set export format — CSV export is available via CLI --export flag
```

## Gap analysis Excel files

For each failed test case, an XLSX file is generated showing the differences between source and expected datasets with side-by-side comparison of values.

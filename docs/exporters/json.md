# JSON exporter

The JSON exporter generates a structured JSON file with detailed results for each test case, plus Excel files for failed tests.

This is the default export format.

## Output structure

```
{output_path}/json/
├── test_results.json             → Structured results for all test cases
└── test_results/
    ├── Test case 1.xlsx          → Gap details (only for failed tests)
    └── Test case 2.xlsx
```

## JSON structure

``` json
[
  {
    "execution_id": "a1b2c3d4-...",
    "name": "Test case name",
    "state": "passed",
    "source": {
      "start": "2024-02-05T17:08:36Z",
      "end": "2024-02-05T17:08:36Z",
      "duration": 0.003298,
      "count": 150,
      "executed_action": "SELECT * FROM employees"
    },
    "expected": {
      "start": "2024-02-05T17:08:36Z",
      "end": "2024-02-05T17:08:36Z",
      "duration": 0.000061,
      "count": 150,
      "executed_action": "./data/expected.csv"
    },
    "compare": {
      "start": "2024-02-05T17:08:36Z",
      "end": "2024-02-05T17:08:36Z",
      "duration": 0.000465,
      "success_rate": 1.0
    },
    "error": {
      "type": null,
      "message": null,
      "detail_file_path": null
    }
  }
]
```

## JSON properties

| Property | Description |
|----------|-------------|
| `execution_id` | Unique identifier for the test run |
| `name` | Test case name |
| `state` | Result: `passed`, `failed`, `error`, `notExecuted` |
| `source.start` / `end` / `duration` | Source loading timing |
| `source.count` | Number of rows in source dataset |
| `source.executed_action` | Query or path executed |
| `expected.start` / `end` / `duration` | Expected loading timing |
| `expected.count` | Number of rows in expected dataset |
| `expected.executed_action` | Query or path executed |
| `compare.start` / `end` / `duration` | Comparison timing |
| `compare.success_rate` | Percentage of matching rows |
| `error.type` | Error category: `headers`, `count`, `data`, `compare` |
| `error.message` | Error description |
| `error.detail_file_path` | Path to XLSX gap analysis file |

## Usage

### Command line

``` shell
ploosh --connections connections.yml --cases test_cases --export JSON
```

JSON is the default format, so `--export` can be omitted.

## Gap analysis Excel files

For each failed test case, an XLSX file is generated showing the differences between source and expected datasets with side-by-side comparison of values.

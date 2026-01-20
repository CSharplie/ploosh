# Structure
```
output/
├─ json/
│  ├─ test_results.json
│  ├─ test_results/
│  │  ├─ test case 1.xlsx
│  │  ├─ test case 2.xlsx
│  │  └─ ...
```

The json extractor will generate a `test_results.json` file and a `test_results` folder containing the details of the test cases results in xlsx format.

# test_results.json
The `test_results.json` file will contain the following properties:
- `execution_id`: the unique execution identifier for this test run
- `name`: the name of the test case
- `state`: the state of the test case. Can be `passed`, `failed` or `error`
- `error.type`: the type of the error if the test case failed or raised an error
- `error.message`: the error message if the test case failed or raised an error
- `error.detail_file_path`: the path to the Excel file containing the comparison gap details (only present when there are data mismatches)
- `source.start`: the start time of the source extraction
- `source.end`: the end time of the source extraction
- `source.duration`: the duration of the source extraction
- `source.count`: the count of the source dataset
- `source.executed_action`: the executed action for the source (SQL query, file path, etc.)
- `expected.start`: the start time of the expected extraction
- `expected.end`: the end time of the expected extraction
- `expected.duration`: the duration of the expected extraction
- `expected.count`: the count of the expected dataset
- `expected.executed_action`: the executed action for the expected dataset (SQL query, file path, etc.)
- `compare.start`: the start time of the comparison
- `compare.end`: the end time of the comparison
- `compare.duration`: the duration of the comparison
- `compare.success_rate`: the success rate of the test case

# test_results folder
The `test_results` folder will contain one xlsx file per test case. Each file will contain a sheet with the gap between the source and the expected dataset

# Example
``` json
[
  {
    "execution_id": "test_execution_123",
    "name": "test 1",
    "state": "passed",
    "source": {
      "start": "2024-02-05T17:08:36Z",
      "end": "2024-02-05T17:08:36Z",
      "duration": 0.0032982,
      "count": 100,
      "executed_action": "SELECT * FROM table1"
    },
    "expected": {
      "start": "2024-02-05T17:08:36Z",
      "end": "2024-02-05T17:08:36Z",
      "duration": 6.0933333333333335e-05,
      "count": 100,
      "executed_action": "SELECT * FROM table2"
    },
    "compare": {
      "start": "2024-02-05T17:08:36Z",
      "end": "2024-02-05T17:08:36Z",
      "duration": 0.0032982,
      "success_rate": 1.0
    }
  },
  {
    "execution_id": "test_execution_123",
    "name": "test 2",
    "state": "failed",
    "source": {
      "start": "2024-02-05T17:08:36Z",
      "end": "2024-02-05T17:08:36Z",
      "duration": 0.0032982,
      "count": 100,
      "executed_action": "SELECT * FROM table1"
    },
    "expected": {
      "start": "2024-02-05T17:08:36Z",
      "end": "2024-02-05T17:08:36Z",
      "duration": 6.0933333333333335e-05,
      "count": 100,
      "executed_action": "SELECT * FROM table2"
    },
    "compare": {
      "start": "2024-02-05T17:08:36Z",
      "end": "2024-02-05T17:08:36Z",
      "duration": 0.0032982,
      "success_rate": 0.95
    },
    "error": {
      "type": "Data",
      "message": "Some rows are not equals between source dataset and expected dataset",
      "detail_file_path": "/output/json/test_results/test 2.xlsx"
    }
  }
]
```
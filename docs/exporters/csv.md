# Structure
```
output/
├─ csv/
│  ├─ test_results.csv
│  ├─ test_results/
│  │  ├─ test case 1.xlsx
│  │  ├─ test case 2.xlsx
│  │  └─ ...
```

The csv extractor will generate a `test_results.csv` file and a `test_results` folder containing the details of the test cases results in xlsx format.

# test_results.csv
The `test_results.csv` file will contain the following columns:
- `execution_id`: the unique execution identifier for this test run
- `name`: the name of the test case
- `state`: the state of the test case. Can be `passed`, `failed` or `error`
- `source_start`: the start time of the source extraction
- `source_end`: the end time of the source extraction
- `source_duration`: the duration of the source extraction
- `source_count`: the count of the source dataset
- `source_executed_action`: the executed action for the source (SQL query, file path, etc.)
- `expected_start`: the start time of the expected extraction
- `expected_end`: the end time of the expected extraction
- `expected_duration`: the duration of the expected extraction
- `expected_count`: the count of the expected dataset
- `expected_executed_action`: the executed action for the expected dataset (SQL query, file path, etc.)
- `compare_start`: the start time of the comparison
- `compare_end`: the end time of the comparison
- `compare_duration`: the duration of the comparison
- `success_rate`: the success rate of the test case
- `error_type`: the type of the error if the test case failed or raised an error
- `error_message`: the error message if the test case failed or raised an error
- `error_detail_file_path`: the path to the Excel file containing the comparison gap details (only present when there are data mismatches)
# test_results folder
The `test_results` folder will contain one xlsx file per test case. Each file will contain a sheet with the gap between the source and the expected dataset

# Example
``` csv
execution_id,name,state,source_start,source_end,source_duration,source_count,source_executed_action,expected_start,expected_end,expected_duration,expected_count,expected_executed_action,compare_start,compare_end,compare_duration,success_rate,error_type,error_message,error_detail_file_path
test_execution_123,test 1,passed,2024-02-05T17:08:36Z,2024-02-05T17:08:36Z,0.0032982,100,SELECT * FROM table1,2024-02-05T17:08:36Z,2024-02-05T17:08:36Z,6.0933333333333335e-05,100,SELECT * FROM table2,2024-02-05T17:08:36Z,2024-02-05T17:08:36Z,0.0032982,1.0,,,
test_execution_123,test 2,failed,2024-02-05T17:08:36Z,2024-02-05T17:08:36Z,0.0032982,100,SELECT * FROM table1,2024-02-05T17:08:36Z,2024-02-05T17:08:36Z,6.0933333333333335e-05,100,SELECT * FROM table2,2024-02-05T17:08:36Z,2024-02-05T17:08:36Z,0.0032982,0.95,Data,Some rows are not equals between source dataset and expected dataset,/output/csv/test_results/test 2.xlsx
```
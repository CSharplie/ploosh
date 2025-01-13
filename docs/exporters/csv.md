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
- `test_case`: the name of the test case
- `status`: the status of the test case. Can be `success`, `failure` or `error`
- `source_start`: the start time of the source extraction
- `source_end`: the end time of the source extraction
- `source_duration`: the duration of the source extraction
- `source_count`: the count of the source dataset
- `expected_start`: the start time of the expected extraction
- `expected_end`: the end time of the expected extraction
- `expected_duration`: the duration of the expected extraction
- `expected_count`: the count of the expected dataset
- `success_rate`: the success rate of the test case
- `error_type`: the type of the error if the test case failed or raised an error
- `error_message`: the error message if the test case failed or raised an error
- 
# test_results folder
The `test_results` folder will contain one xlsx file per test case. Each file will contain a sheet with the gap between the source and the expected dataset

# Example
``` csv
test_case,status,source_start,source_end,source_duration,source_count,expected_start,expected_end,expected_duration,expected_count,success_rate,error_type,error_message
test 1,passed,2024-02-05T17:08:36Z,2024-02-05T17:08:36Z,0.0032982,100,2024-02-05T17:08:36Z,2024-02-05T17:08:36Z,6.0933333333333335e-05,100,1.0,,,
test 2,failed,2024-02-05T17:08:36Z,2024-02-05T17:08:36Z,0.0032982,100,2024-02-05T17:08:36Z,2024-02-05T17:08:36Z,6.0933333333333335e-05,100,0.95,Data,Some rows are not equals between source dataset and expected dataset
```
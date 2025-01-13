# Structure
```
output/
├─ trx/
│  ├─ test_results.xml
│  ├─ test_results/
│  │  ├─ execution ID (guid)/
│  │  │  ├─ test case 1.xlsx
│  │  ├─ execution ID (guid)/
│  │  │  ├─ test case 2.xlsx
│  │  └─ ...
```

# test_results.xml
The `test_results.xml` file use the TRX format (Visual Studio Test Results File). It will contain the details of the test cases results in XML format.

This file can be opened with Visual Studio or any other tool that support the TRX format. 

It can be used with Azure DevOps to publish the test results.

# test_results folder
The `test_results` folder will contain one xlsx file per test case. Each file will contain a sheet with the gap between the source and the expected dataset
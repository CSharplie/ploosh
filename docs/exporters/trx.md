# TRX exporter

The TRX exporter generates test results in the Visual Studio Test Results (TRX) XML format. This format is compatible with Azure DevOps Test Plans and Visual Studio.

## Output structure

```
{output_path}/trx/
├── test_results.xml                          → TRX results file
└── test_results/
    └── In/
        └── {execution_id}/
            ├── Test case 1.xlsx              → Gap details (only for failed tests)
            └── Test case 2.xlsx
```

## TRX format

The XML file follows the Visual Studio TestRun schema and includes:

- **TestSettings**: Execution settings
- **ResultSummary**: Counters for total, executed, passed, failed, error, and notExecuted tests
- **TestDefinitions**: One entry per test case
- **Results**: Outcome, duration, and error details per test
- **TestEntries**: Links between definitions and results

## Usage

### Command line

``` shell
ploosh --connections connections.yml --cases test_cases --export TRX
```

### Azure DevOps integration

The TRX format integrates directly with Azure DevOps Test Plans using the `PublishTestResults` task:

``` yaml
- task: PublishTestResults@2
  inputs:
    testResultsFormat: 'VSTest'
    testResultsFiles: '*.xml'
    searchFolder: 'output/trx/'
    mergeTestResults: true
    testRunTitle: '$(Build.DefinitionName)'
```

See [Azure DevOps pipeline](/docs/pipelines/azure-devops) for a complete pipeline example.

## Gap analysis Excel files

For each failed test case, an XLSX file is generated in the `test_results/In/{execution_id}/` folder, showing a side-by-side comparison of differing values between source and expected datasets.

# Fabric reporting

By persisting Ploosh test results into a Delta table (see [Fabric notebook](/docs/spark/fabric-notebook)), you can build Power BI reports to monitor data quality over time.

## Semantic model

Create a Semantic Model on top of the `ploosh_results` Delta table in your Lakehouse:

1. In your Ploosh workspace, click **New** → **Semantic model**
2. Select the `ploosh_results` table from the Lakehouse
3. Define a date hierarchy on `execution_date` for time-based analysis
4. Publish the model

## Suggested measures

| Measure | DAX formula |
|---------|-------------|
| Total tests | `COUNTROWS('ploosh_results')` |
| Passed tests | `CALCULATE(COUNTROWS('ploosh_results'), 'ploosh_results'[state] = "passed")` |
| Failed tests | `CALCULATE(COUNTROWS('ploosh_results'), 'ploosh_results'[state] = "failed")` |
| Error tests | `CALCULATE(COUNTROWS('ploosh_results'), 'ploosh_results'[state] = "error")` |
| Pass rate | `DIVIDE([Passed tests], [Total tests], 0)` |
| Avg source duration | `AVERAGE('ploosh_results'[source_duration])` |
| Avg compare duration | `AVERAGE('ploosh_results'[compare_duration])` |

## Dashboard layout

A typical data quality dashboard includes:

### Overview page
- **KPI cards**: Total tests, pass rate, failed count, error count
- **Trend chart**: Pass rate over time (by `execution_date`)
- **Table**: Latest execution results with state, duration, and error details

### Detail page
- **Filter by test name**: Drill into a specific test case history
- **Duration chart**: Source/expected/compare durations over time
- **Error breakdown**: Error types distribution (headers, count, data, compare)

### Operational page
- **Execution timeline**: Gantt-style view of test execution times
- **Success rate heatmap**: Success rates by test case and date
- **Alert list**: Tests with success rate below threshold

## Alerting

Use Power BI data alerts or Fabric Data Activator to trigger notifications when:

- A test case fails for the first time
- The overall pass rate drops below a threshold
- A test case duration exceeds a limit (potential performance regression)

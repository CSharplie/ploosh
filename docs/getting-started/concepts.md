# Core concepts

## Test case

A test case is defined in a YAML file and consists of:

- A **source**: the data to validate (query result, file content, etc.)
- An **expected**: the reference data to compare against
- **Options** (optional): comparison settings (sort, cast, ignore, tolerance, etc.)

``` yaml
My test case:
  disabled: false
  options:
    sort:
      - column1
  source:
    type: mysql
    connection: my_connection
    query: SELECT * FROM my_table
  expected:
    type: csv
    path: ./expected_data.csv
```

## Connectors

A connector defines how to read data from a source. Each connector has:

- A **type** identifier (e.g. `mysql`, `csv`, `parquet_spark`)
- Optional **connection parameters** (hostname, credentials, etc.) defined in a connections file
- **Configuration parameters** (query, path, etc.) defined in the test case

There are two families of connectors:

| Family | Engine | Connectors |
|--------|--------|------------|
| **Native** | Pandas | CSV, JSON, Parquet, Delta, Excel, Empty, MySQL, PostgreSQL, SQL Server, Snowflake, BigQuery, Databricks, ODBC, Analysis Services, Semantic Model |
| **Spark** | PySpark | CSV Spark, JSON Spark, Parquet Spark, Delta Spark, Empty Spark, SQL Spark, Fabric KQL Spark, Dremio Spark |

> ⚠️ Both source and expected must use the same family. You cannot mix a native connector with a Spark connector in the same test case.

## Connections

Connections are defined in a separate YAML file and contain the parameters needed to connect to data sources (hostnames, credentials, ports, etc.). They are referenced by name in the test case configuration.

``` yaml
my_connection:
  type: mysql
  hostname: server.database.windows.net
  database: my_db
  username: user
  password: $var.db_password
```

## Compare engine

The compare engine validates that source and expected datasets match. The comparison process follows three steps:

1. **Structure check**: Verify that both datasets have the same columns (case-insensitive, trimmed).
2. **Row count check**: Verify that both datasets have the same number of rows.
3. **Data comparison**: Compare data row by row, applying preprocessing options (trim, case_insensitive, tolerance).

### Compare modes

| Mode | Description | Available in |
|------|-------------|--------------|
| **order** | Row-by-row comparison based on row position or sort order | Native, Spark |
| **join** | Match rows by join keys instead of position | Spark only |

## Test case states

| State | Description |
|-------|-------------|
| `passed` | Source and expected datasets match |
| `failed` | Differences found between datasets |
| `error` | An exception occurred during execution |
| `notExecuted` | Test case is disabled |

## Error types

When a test case fails or errors, an error type indicates the stage where the issue occurred:

| Error type | Description |
|------------|-------------|
| `headers` | Column structure mismatch |
| `count` | Row count mismatch |
| `data` | Data values differ between source and expected |
| `compare` | Exception during comparison |

## Exporters

Exporters save test results to files. All exporters also generate **Excel files (`.xlsx`)** with detailed gap analysis for failed test cases.

| Format | Output file | Description |
|--------|-------------|-------------|
| JSON | `test_results.json` | Structured results with nested objects |
| CSV | `test_results.csv` | Flattened results, one row per test |
| TRX | `test_results.xml` | Visual Studio Test Results format, compatible with Azure DevOps |

For each failed test, an `.xlsx` file is generated containing only the rows and columns that differ, with `{column}_source` and `{column}_expected` side by side. This makes it easy to identify exactly where source and expected data diverge.

## Custom parameters

Variables can be used in YAML files with the `$var.<name>` syntax and passed at runtime via `--p_<name>` arguments. This avoids hardcoding sensitive information like passwords.

``` yaml
# In connections.yml
my_connection:
  type: mysql
  password: $var.db_password
```

``` shell
# At runtime
ploosh --connections connections.yml --cases test_cases --p_db_password "secret"
```

# Quick start

This guide walks you through your first test case with Ploosh in 5 steps.

## 1. Install Ploosh

``` shell
pip install ploosh
```

## 2. Setup connection file

Create a file `connections.yml` with your database connections:

``` yaml
my_database:
  type: mysql
  hostname: my_server.database.windows.net
  database: my_database_name
  username: my_user_name
  password: $var.db_password
```

> Using `$var.db_password` instead of a hardcoded password allows you to pass it securely via the command line at runtime.

## 3. Create test cases

Create a folder `test_cases/` and add a YAML file (e.g. `tests.yml`) with your test definitions:

``` yaml
Test aggregated data:
  options:
    sort:
      - gender
      - domain
  source:
    connection: my_database
    type: mysql
    query: |
      SELECT gender,
             RIGHT(email, LENGTH(email) - POSITION("@" IN email)) AS domain,
             COUNT(*) AS count
      FROM users
      GROUP BY gender, domain
  expected:
    type: csv
    path: ./data/expected_aggregation.csv

Test no invalid emails:
  source:
    connection: my_database
    type: mysql
    query: |
      SELECT *
      FROM users
      WHERE email NOT LIKE '%@%.%'
  expected:
    type: empty
```

## 4. Run tests

``` shell
ploosh --connections "connections.yml" --cases "test_cases" --export "JSON" --p_db_password "my_secret_password"
```

During execution, the status of each test is displayed in real-time:

```
 ____  _                 _
|  _ \| | ___   ___  ___| |__
| |_) | |/ _ \ / _ \/ __| '_ \
|  __/| | (_) | (_) \__ \ | | |
|_|   |_|\___/ \___/|___/_| |_|

Initialization[...]
Start processing tests cases[...]
Test aggregated data [...] (1/2) - Started
Test aggregated data [...] (1/2) - Passed
Test no invalid emails [...] (2/2) - Started
Test no invalid emails [...] (2/2) - Passed
Summary[...]
Total: 2 | Passed: 2 | Failed: 0 | Error: 0
```

## 5. Review results

A `test_results.json` file is generated in the `output/json/` folder:

``` json
[
  {
    "name": "Test aggregated data",
    "state": "passed",
    "source": {
      "start": "2024-02-05T17:08:36Z",
      "end": "2024-02-05T17:08:36Z",
      "duration": 0.003298
    },
    "expected": {
      "start": "2024-02-05T17:08:36Z",
      "end": "2024-02-05T17:08:36Z",
      "duration": 0.000061
    },
    "compare": {
      "start": "2024-02-05T17:08:36Z",
      "end": "2024-02-05T17:08:36Z",
      "duration": 0.000465
    }
  }
]
```

### Gap analysis Excel files

When a test fails, an Excel file (`.xlsx`) is automatically generated in `output/json/test_results/` with a detailed gap analysis. The file contains a side-by-side comparison of the differing values:

| Column | Description |
|--------|-------------|
| `{column}_source` | Value from the source dataset |
| `{column}_expected` | Value from the expected dataset |

Only rows and columns with differences are included, making it easy to pinpoint exactly where the data diverges.

## Next steps

- [Command line options](/docs/configuration/command-line) — All CLI arguments
- [Test case options](/docs/configuration/options) — Sort, cast, ignore, tolerance, etc.
- [Custom parameters](/docs/configuration/custom-parameters) — Secure variable substitution
- [Spark mode](/docs/spark/overview) — Run Ploosh on Microsoft Fabric or Databricks

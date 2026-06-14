# PostgreSQL exporter

The PostgreSQL exporter writes test case results into a PostgreSQL database table instead of a file. It reuses the [PostgreSQL connector](/docs/connectors/native/postgresql) to connect and run the queries.

The exporter automatically creates the destination table if it does not exist, then inserts one row per test case.

## Connection configuration

The exporter connects through a dedicated `__export__` connection declared in the connections file. The `type` of this connection must match the exporter name (`postgresql`).

The connection accepts the same parameters as the [PostgreSQL connector](/docs/connectors/native/postgresql).

``` yaml
connections:
  __export__:
    type: postgresql
    hostname: my-server.postgres.database.azure.com
    database: my_database
    username: my_user
    password: $var.postgresql_password
    port: 5432
    ssl_context: false
```

## Destination table

The exporter writes results to a table named `ploosh_results`. The table is created automatically with the following schema:

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

## Usage

### Command line

``` shell
ploosh --connections connections.yml --cases test_cases --export POSTGRESQL --p_postgresql_password "your_password"
```

### Python API

``` python
from ploosh import execute_cases

execute_cases(
    cases="test_cases",
    connections="connections.yml",
    export="POSTGRESQL",
    variables={"postgresql_password": "your_password"}
)
```

## Requirements

- PostgreSQL optional dependency installed (`pip install ploosh[postgresql]` or `pip install pg8000`)
- A `__export__` connection of type `postgresql` declared in the connections file
- Network access to the PostgreSQL database server

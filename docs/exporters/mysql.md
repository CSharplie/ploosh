# MySQL exporter

The MySQL exporter writes test case results into a MySQL database table instead of a file. It reuses the [MySQL connector](/docs/connectors/native/mysql) to connect and run the queries.

The exporter automatically creates the destination table if it does not exist, then inserts one row per test case.

## Connection configuration

The exporter connects through a dedicated `__export__` connection declared in the connections file. The `type` of this connection must match the exporter name (`mysql`).

The connection accepts the same parameters as the [MySQL connector](/docs/connectors/native/mysql).

``` yaml
connections:
  __export__:
    type: mysql
    hostname: my-server.database.windows.net
    database: my_database
    username: my_user
    password: $var.mysql_password
    port: 3306
```

## Destination table

The exporter writes results to a table named `ploosh_results` by default. You can change this name by setting the `table` parameter in the connection configuration.

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
ploosh --connections connections.yml --cases test_cases --export MYSQL
```

## Requirements

- MySQL optional dependency installed (`pip install ploosh[mysql]`)
- A `__export__` connection of type `mysql` declared in the connections file

# Spark mode overview

Ploosh supports two execution modes: **Native** (Pandas) and **Spark** (PySpark). Spark mode is designed to run within distributed environments like **Microsoft Fabric**, **Databricks**, or a **local Spark session**, enabling validation of large-scale datasets.

## Why Spark mode?

| Benefit | Description |
|---------|-------------|
| **Distributed processing** | Leverage Spark clusters to validate large volumes of data |
| **Native platform access** | Query Lakehouse tables, KQL databases, and Delta files directly |
| **No data movement** | Data stays within the platform, avoiding costly exports |
| **Integrated execution** | Run tests directly from notebooks alongside your data pipelines |

## When to use Spark mode?

| Scenario | Recommended mode |
|----------|-----------------|
| CI/CD pipeline on a build agent | Native |
| Local development with small datasets | Native |
| Microsoft Fabric notebooks | **Spark** |
| Databricks notebooks | **Spark** |
| Large datasets (millions of rows) | **Spark** |
| Querying Lakehouse/KQL/Delta files on a cluster | **Spark** |

## Spark connectors

Spark mode uses dedicated connectors. You **cannot** mix Spark and native connectors in the same test case.

| Connector | Type | Description |
|-----------|------|-------------|
| `csv_spark` | File | Read CSV files via Spark |
| `json_spark` | File | Read JSON files via Spark |
| `parquet_spark` | File | Read Parquet files via Spark |
| `delta_spark` | File | Read Delta tables via Spark |
| `sql_spark` | Query | Execute Spark SQL queries |
| `fabric_kql_spark` | Database | Query Fabric KQL databases |
| `dremio_spark` | Database | Query Dremio via Arrow Flight SQL |
| `empty_spark` | Utility | Return an empty DataFrame |

## Spark comparison engine

The Spark compare engine supports two comparison modes:

| Mode | Description |
|------|-------------|
| **order** (default) | Rows are matched by position using a `row_number()` window function |
| **join** | Rows are matched by specified `join_keys` columns (Spark only) |

The **join** mode is particularly useful when row ordering is not deterministic or when matching by business keys is more appropriate.

``` yaml
My test case:
  options:
    compare_mode: join
    join_keys:
      - employee_id
  source:
    type: sql_spark
    query: SELECT * FROM lakehouse.employees
  expected:
    type: csv_spark
    path: /lakehouse/default/Files/expected/employees.csv
```

## Calling Ploosh from Python

In Spark mode, Ploosh is called programmatically from Python using the `execute_cases()` function:

``` python
from ploosh import execute_cases

execute_cases(
    cases="/path/to/cases",
    connections="/path/to/connections.yaml",
    spark_session=spark,
    filter="*.yaml",
    path_output="/path/to/output"
)
```

See the [Python API reference](/docs/api/execute-cases) for full details.

## Platform-specific guides

- [Microsoft Fabric setup](/docs/spark/fabric-setup) — Complete guide for Fabric
- [Fabric notebook orchestration](/docs/spark/fabric-notebook) — Notebook implementation
- [Fabric shortcuts strategy](/docs/spark/fabric-shortcuts) — Cross-workspace data access
- [Fabric reporting](/docs/spark/fabric-reporting) — Power BI dashboards on test results
- [Databricks setup](/docs/spark/databricks) — Running Ploosh on Databricks
- [Local Spark](/docs/spark/local-spark) — Running Ploosh with a local SparkSession

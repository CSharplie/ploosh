# Ploosh documentation

Ploosh is a YAML-based automated testing framework for data projects. It compares source datasets against expected results across databases, files, and cloud platforms — in both **native (Pandas)** and **Spark** modes.

## Get started

1. [What is Ploosh?](/docs/getting-started/what-is-ploosh) — Overview, key concepts, and architecture
2. [Installation](/docs/getting-started/installation) — Install from PyPi
3. [Quick start](/docs/getting-started/quick-start) — Your first test case in 5 minutes
4. [Core concepts](/docs/getting-started/concepts) — Connectors, engines, exporters, states

## Spark mode & Microsoft Fabric

Ploosh runs natively on Spark for validating large-scale data platforms.

- [Spark mode overview](/docs/spark/overview) — Why Spark, when to use it, Spark connectors
- [Microsoft Fabric setup](/docs/spark/fabric-setup) — Complete Fabric architecture guide
- [Fabric notebook](/docs/spark/fabric-notebook) — Orchestration notebook with results history
- [Fabric shortcuts](/docs/spark/fabric-shortcuts) — Cross-workspace data access strategy
- [Fabric reporting](/docs/spark/fabric-reporting) — Power BI dashboard on test results
- [Databricks](/docs/spark/databricks) — Running Ploosh on Databricks
- [Local Spark](/docs/spark/local-spark) — Development with local SparkSession

## Configuration

- [Command line](/docs/configuration/command-line) — CLI arguments and Python API
- [Test case options](/docs/configuration/options) — Sort, cast, ignore, tolerance, compare_mode, join_keys, etc.
- [Custom parameters](/docs/configuration/custom-parameters) — Secure variable substitution

## Connectors

### Native connectors (Pandas)

| Type | Connectors |
|------|------------|
| Databases | [BigQuery](/docs/connectors/native/big-query), [Databricks](/docs/connectors/native/databricks), [Snowflake](/docs/connectors/native/snowflake), [SQL Server](/docs/connectors/native/sqlserver), [PostgreSQL](/docs/connectors/native/postgresql), [MySQL](/docs/connectors/native/mysql), [ODBC](/docs/connectors/native/odbc) |
| Files | [CSV](/docs/connectors/native/csv), [Excel](/docs/connectors/native/excel), [JSON](/docs/connectors/native/json), [Parquet](/docs/connectors/native/parquet), [Delta](/docs/connectors/native/delta) |
| BI Tools | [Analysis Services](/docs/connectors/native/analysis-services), [Semantic Model (XMLA)](/docs/connectors/native/semantic-model-xmla) |
| Utilities | [Empty](/docs/connectors/native/empty) |

### Spark connectors

| Type | Connectors |
|------|------------|
| Databases | [SQL Spark](/docs/connectors/spark/sql), [Dremio](/docs/connectors/spark/dremio), [Fabric KQL](/docs/connectors/spark/fabric-kql) |
| Files | [CSV](/docs/connectors/spark/csv), [JSON](/docs/connectors/spark/json), [Parquet](/docs/connectors/spark/parquet), [Delta](/docs/connectors/spark/delta) |
| Utilities | [Empty](/docs/connectors/spark/empty) |

## Exporters

- [JSON](/docs/exporters/json) — Default format, structured results
- [CSV](/docs/exporters/csv) — Flat file format
- [TRX](/docs/exporters/trx) — Visual Studio Test Results, Azure DevOps compatible

## CI/CD Pipelines

- [Azure DevOps](/docs/pipelines/azure-devops) — Pipeline with TRX publishing
- [GitHub Actions](/docs/pipelines/github-actions) — Workflow with artifact upload
- [Fabric Pipeline](/docs/pipelines/fabric-pipeline) — Notebook orchestration in Fabric

## Use cases

- [Testing approaches](/docs/use-cases/testing-approaches) — By recalculation, by empty, by test data
- [Migration testing](/docs/use-cases/migration-testing) — Legacy vs target comparison
- [Fabric data platform](/docs/use-cases/fabric-data-platform) — End-to-end Fabric validation
- [Regression testing](/docs/use-cases/regression-testing) — Continuous test suites
- [Data quality](/docs/use-cases/data-quality) — Anomalies, duplicates, completeness

## API reference

- [execute_cases()](/docs/api/execute-cases) — Python API for notebook execution
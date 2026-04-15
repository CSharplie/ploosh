# What is Ploosh?

Ploosh is an automated testing framework designed for data projects. Based on YAML configuration files, it enables teams to quickly and simply define, execute, and report on data validation tests.

## Why Ploosh?

Testing tools for application development are not necessarily suited for data and BI projects. Data systems are often chains of complex workflows with multiple dependencies, making it difficult to test the entire process. In the traditional development world, we are used to the sequence: CI (build & tests) / deployment / execution. In data projects, this becomes: CI (build only) / deployment / execution / tests.

Ploosh fills this gap by providing a dedicated framework for data testing.

## Key benefits

- **Reduce testing effort**: With industrialized tests, teams can focus on development or creating complex and high-value test cases.
- **Reduce regression risks**: By continuously running tests, regressions can be detected quickly and fixed before they impact production.
- **Increase test quality**: When a new bug is detected, new test cases can be added to the framework to prevent recurrence.
- **Improve project quality**: With fewer regression bugs and a more efficient team, the product's quality improves.

## How it works

A test case consists of two parts: a **source** (the data to validate) and an **expected** (the reference data). For a test to pass, the source must match the expected.

The framework offers three main components:

1. **Connectors**: Query data sources (databases, files, APIs) and store the result in a homogeneous format (DataFrame).
2. **Compare engine**: Compare, for each test case, the source data with the expected data through three successive steps: row count comparison, structural equality check, and row-by-row data comparison.
3. **Exporters**: Export test results in different formats (JSON, CSV, TRX) for integration with reporting tools or CI/CD pipelines.

## Two execution modes

Ploosh provides two execution modes to adapt to different environments:

| Mode | Engine | Best for |
|------|--------|----------|
| **Native** | Pandas | Local execution, CI/CD agents, small to medium datasets |
| **Spark** | PySpark | Microsoft Fabric, Databricks, large distributed datasets |

> ⚠️ A Spark connector can only be used with another Spark connector. It is not possible to mix Spark and native connectors in the same test case.

## Supported connectors

| Type | Native connectors | Spark connectors |
|-----------|-------------------|------------------|
| Databases | BigQuery, Databricks, Snowflake, SQL Server, PostgreSQL, MySQL, ODBC | SQL Spark, Dremio |
| Files | CSV, Excel, JSON, Parquet, Delta | CSV, JSON, Parquet, Delta |
| BI Tools | Analysis Services, Semantic Model (XMLA) | Fabric KQL |
| Utilities | Empty | Empty |

## Supported export formats

| Format | Description |
|--------|-------------|
| JSON | JSON file with detailed results |
| CSV | CSV file with flattened results |
| TRX | Visual Studio Test Results XML format, compatible with Azure DevOps Test Plans |

All export formats also generate Excel files (XLSX) with detailed gap analysis for failed test cases.

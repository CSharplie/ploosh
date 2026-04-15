# SQL (Spark)

This connector is used to execute Spark SQL queries. It is the primary connector for querying Lakehouse tables in Microsoft Fabric or registered tables in Databricks.

> ⚠️ A Spark connector can only be used with another Spark connector. It is not possible to mix Spark and native connectors in the same test case.

See [Spark mode overview](/docs/spark/overview) for more information.

## Connection configuration

No connection is required by this connector.

## Test case configuration

| Name | Mandatory | Default | Description |
|------|:---------:|:-------:|-------------|
| query | yes | | Spark SQL query to execute |

### Example

``` yaml
Example SQL Spark:
  source:
    type: sql_spark
    query: |
      SELECT department, COUNT(*) AS count
      FROM lakehouse.employees
      GROUP BY department
  expected:
    type: csv_spark
    path: /lakehouse/default/Files/expected/department_counts.csv
    header: true
    inferSchema: true
```

### Example with Fabric shortcuts

When using shortcuts in Microsoft Fabric, remote Lakehouse tables are queryable as local tables:

``` yaml
Test cross-workspace data:
  source:
    type: sql_spark
    query: |
      SELECT *
      FROM dw_lakehouse.fact_sales
      WHERE sale_date >= '2024-01-01'
  expected:
    type: sql_spark
    query: |
      SELECT *
      FROM reporting_lakehouse.fact_sales_report
      WHERE sale_date >= '2024-01-01'
```

See [Fabric shortcuts strategy](/docs/spark/fabric-shortcuts) for more details.

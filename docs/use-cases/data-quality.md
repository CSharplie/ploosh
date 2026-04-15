# Data quality checks

Ploosh can be used for operational data quality monitoring, ensuring data consistency, completeness, and correctness across your data platform.

## Approaches

### Absence of anomalies (empty approach)

Use the `empty` connector to verify that no problematic data exists:

``` yaml
Test no NULL emails:
  source:
    connection: dwh
    type: mssql
    query: |
      SELECT *
      FROM dim_customer
      WHERE email IS NULL AND is_active = 1
  expected:
    type: empty

Test no duplicate customer IDs:
  source:
    connection: dwh
    type: mssql
    query: |
      SELECT customer_id, COUNT(*) AS cnt
      FROM dim_customer
      GROUP BY customer_id
      HAVING COUNT(*) > 1
  expected:
    type: empty

Test no future dates:
  source:
    connection: dwh
    type: mssql
    query: |
      SELECT *
      FROM fact_orders
      WHERE order_date > GETDATE()
  expected:
    type: empty
```

### Completeness checks

Verify that record counts match across layers:

``` yaml
Test row count consistency:
  source:
    connection: raw
    type: mssql
    query: |
      SELECT source_table, COUNT(*) AS row_count
      FROM raw.load_log
      WHERE load_date = CAST(GETDATE() AS DATE)
      GROUP BY source_table
      ORDER BY source_table
  expected:
    connection: dwh
    type: mssql
    query: |
      SELECT source_table, COUNT(*) AS row_count
      FROM dwh.load_log
      WHERE load_date = CAST(GETDATE() AS DATE)
      GROUP BY source_table
      ORDER BY source_table
```

### Referential integrity

Verify that foreign key relationships are respected:

``` yaml
Test no orphan orders:
  source:
    connection: dwh
    type: mssql
    query: |
      SELECT f.order_id, f.product_id
      FROM fact_orders f
      LEFT JOIN dim_product p ON f.product_id = p.product_id
      WHERE p.product_id IS NULL
  expected:
    type: empty
```

### Range validation

Verify that values fall within expected ranges:

``` yaml
Test valid percentages:
  source:
    connection: dwh
    type: mssql
    query: |
      SELECT *
      FROM fact_metrics
      WHERE success_rate < 0 OR success_rate > 1
  expected:
    type: empty
```

## Spark mode for Fabric

The same quality checks work in Microsoft Fabric with Spark connectors:

``` yaml
Test no NULL customer IDs (Fabric):
  source:
    type: sql_spark
    query: |
      SELECT *
      FROM lakehouse.dim_customer
      WHERE customer_id IS NULL
  expected:
    type: empty_spark
```

See [Testing a Fabric data platform](/docs/use-cases/fabric-data-platform) for a complete Fabric use case.

## Scheduling quality checks

For operational monitoring, schedule quality checks to run regularly:

- **Daily**: After nightly batch processing completes
- **After each pipeline run**: As a post-processing step
- **On demand**: When investigating data issues

Use the `disabled` option to temporarily skip checks that are under investigation:

``` yaml
Temporarily disabled check:
  disabled: true
  source:
    connection: dwh
    type: mssql
    query: SELECT * FROM problematic_table
  expected:
    type: empty
```

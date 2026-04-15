# Testing a Fabric data platform

This guide demonstrates a complete use case of Ploosh in Microsoft Fabric: validating workloads that write data to Lakehouse tables and events to KQL databases, distributed across multiple workspaces.

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Ingestion WS   │     │  Transform WS   │     │  Reporting WS   │
│  ┌───────────┐  │     │  ┌───────────┐  │     │  ┌───────────┐  │
│  │ Raw       │  │     │  │ DW        │  │     │  │ Datamart   │  │
│  │ Lakehouse │  │     │  │ Lakehouse │  │     │  │ Lakehouse  │  │
│  └───────────┘  │     │  └───────────┘  │     │  └───────────┘  │
└────────┬────────┘     └────────┬────────┘     └────────┬────────┘
         │     shortcuts         │     shortcuts         │
         └───────────────┬───────┴───────────────────────┘
                         │
              ┌──────────▼──────────┐
              │    Ploosh WS        │
              │  ┌───────────────┐  │
              │  │ Ploosh        │  │
              │  │ Lakehouse     │  │
              │  │  ├ cases/     │  │
              │  │  ├ outputs/   │  │
              │  │  └ shortcuts/ │  │
              │  ├───────────────┤  │
              │  │ Notebook      │  │
              │  │ Semantic Model│  │
              │  │ PBI Report    │  │
              │  └───────────────┘  │
              └─────────────────────┘
```

## Test scenarios

### 1. Cross-layer validation

Verify that the transformation layer correctly aggregates raw data:

``` yaml
Test employee aggregation:
  options:
    sort:
      - department
  source:
    type: sql_spark
    query: |
      SELECT department, COUNT(*) AS employee_count
      FROM raw_lakehouse.employees
      GROUP BY department
  expected:
    type: sql_spark
    query: |
      SELECT department, employee_count
      FROM dw_lakehouse.dim_department_summary
```

### 2. KQL event completeness

Verify that pipeline events are correctly logged:

``` yaml
Test pipeline events logged:
  source:
    type: fabric_kql_spark
    connection: kql_events
    query: |
      PipelineEvents
      | where Timestamp > ago(1d)
      | summarize event_count = count() by PipelineName
      | order by PipelineName asc
  expected:
    type: sql_spark
    query: |
      SELECT pipeline_name AS PipelineName, expected_count AS event_count
      FROM ploosh_resources.expected_daily_events
      ORDER BY PipelineName ASC
```

### 3. Data quality checks

Detect anomalies using the empty connector:

``` yaml
Test no NULL customer IDs:
  source:
    type: sql_spark
    query: |
      SELECT *
      FROM dw_lakehouse.fact_orders
      WHERE customer_id IS NULL
  expected:
    type: empty_spark

Test no duplicate orders:
  source:
    type: sql_spark
    query: |
      SELECT order_id, COUNT(*) AS cnt
      FROM dw_lakehouse.fact_orders
      GROUP BY order_id
      HAVING cnt > 1
  expected:
    type: empty_spark
```

### 4. Reference data validation

Compare Lakehouse data against known reference files:

``` yaml
Test product categories:
  options:
    sort:
      - category_id
  source:
    type: sql_spark
    query: |
      SELECT category_id, category_name, is_active
      FROM dw_lakehouse.dim_product_category
  expected:
    type: csv_spark
    path: /lakehouse/default/Files/ploosh_resources/expected_categories.csv
    header: true
    inferSchema: true
```

## Connections file

``` yaml
kql_events:
  type: fabric_kql_spark
  kusto_uri: https://mycluster.kusto.windows.net
  database_id: events_database
```

> Spark SQL queries against Lakehouse tables (via shortcuts) do not require a connection definition.

## Results exploitation

After execution, the results are:
1. **Exported as JSON** for immediate review
2. **Persisted to a Delta table** (`ploosh_results`) for historical tracking
3. **Visualized in Power BI** through a Semantic Model

See [Fabric reporting](/docs/spark/fabric-reporting) for dashboard setup details.

## End-to-end automation

1. **Upstream pipeline** completes data processing
2. **Fabric Pipeline** triggers the Ploosh notebook
3. **Ploosh** executes all test cases and exports results
4. **History tracking** appends results to the Delta table
5. **Power BI** refreshes and shows updated quality metrics
6. **Alerts** notify the team if tests fail

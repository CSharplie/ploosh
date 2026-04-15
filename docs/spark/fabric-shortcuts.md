# Fabric shortcuts strategy

When running Ploosh in Microsoft Fabric, your test cases often need to query data located in **multiple workspaces**. Fabric shortcuts provide a mechanism to make remote data accessible locally without copying it.

## The problem

In a typical Fabric environment, data is distributed across multiple workspaces:

- **Workspace A**: Raw data Lakehouse (ingestion)
- **Workspace B**: Data warehouse / transformed data
- **Workspace C**: Reporting / datamart

Ploosh needs to access tables from all these workspaces to run cross-layer validations.

## The solution: shortcuts

Shortcuts create virtual links to data in other locations, making it queryable via Spark SQL from the Ploosh Lakehouse.

### Types of shortcuts

| Source | Description |
|--------|-------------|
| **OneLake** | Link to another Fabric Lakehouse in the same or different workspace |
| **Azure Data Lake Storage** | Link to ADLS Gen2 storage |
| **Amazon S3** | Link to S3 buckets |

### Creating a shortcut

1. Open your Ploosh Lakehouse
2. In the **Tables** section, click **New shortcut**
3. Select the source type (e.g. OneLake)
4. Navigate to the target workspace and Lakehouse
5. Select the tables to link
6. The tables appear as local tables in your Lakehouse

### Querying shortcut data

Once shortcuts are created, the remote tables are queryable via Spark SQL using the `sql_spark` connector:

``` yaml
Test data warehouse employees:
  source:
    type: sql_spark
    query: |
      SELECT department, COUNT(*) AS count
      FROM dw_lakehouse.employees
      GROUP BY department
  expected:
    type: sql_spark
    query: |
      SELECT department, count
      FROM reporting_lakehouse.employee_summary
```

> No connection configuration is required for `sql_spark` — Spark SQL resolves tables through the Lakehouse metadata.

## Combining shortcuts with KQL

For workloads that write events to KQL databases, use the `fabric_kql_spark` connector alongside `sql_spark`:

``` yaml
connections:
  kql_events:
    type: fabric_kql_spark
    kusto_uri: https://mycluster.kusto.windows.net
    database_id: events_db
```

``` yaml
Test event completeness:
  source:
    type: fabric_kql_spark
    connection: kql_events
    query: |
      ProcessingEvents
      | where Timestamp > ago(1d)
      | summarize event_count = count() by Pipeline
  expected:
    type: sql_spark
    query: |
      SELECT pipeline AS Pipeline, expected_count AS event_count
      FROM ploosh_resources.expected_event_counts
```

## Best practices

- **Organize shortcuts by source workspace**: Create a naming convention (e.g. `dw_lakehouse`, `raw_lakehouse`) to identify origins
- **Use reference tables**: Store expected data as tables or files in the Ploosh Lakehouse for tests that don't compare two live sources
- **Minimize shortcut count**: Only link tables that are actually tested to reduce metadata overhead

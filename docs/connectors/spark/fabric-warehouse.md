# Fabric Warehouse (Spark)

This connector is used to query a Microsoft Fabric Warehouse using Spark via the `sempy_labs` library.

> ⚠️ A Spark connector can only be used with another Spark connector. It is not possible to mix Spark and native connectors in the same test case.

See [Spark mode overview](/docs/spark/overview) for more information.

## Connection configuration

| Name | Mandatory | Default | Description |
|------|:---------:|:-------:|-------------|
| warehouse_name | yes | | Name (or ID) of the Fabric Warehouse to connect to |
| workspace_name | no | `None` | Name (or ID) of the Fabric workspace containing the warehouse (if not specified, uses current workspace) |

### Example

``` yaml
connections:
  fabric_warehouse_connection:
    type: fabric_warehouse_spark
    warehouse_name: my_warehouse
    workspace_name: my_workspace
```

### Example (current workspace)

When `workspace_name` is omitted, the connector uses the current workspace:

``` yaml
connections:
  fabric_warehouse_connection:
    type: fabric_warehouse_spark
    warehouse_name: my_warehouse
```

## Test case configuration

| Name | Mandatory | Default | Description |
|------|:---------:|:-------:|-------------|
| query | yes | | SQL query to execute against the Fabric Warehouse |

### Example

``` yaml
Example Fabric Warehouse Spark:
  source:
    type: fabric_warehouse_spark
    connection: fabric_warehouse_connection
    query: |
      SELECT *
      FROM dbo.employees
      WHERE hire_date < '2000-01-01'
  expected:
    type: sql_spark
    query: |
      SELECT *
      FROM expected_employees
      WHERE hire_date < '2000-01-01'
```

### Example with cross-workspace warehouse

Query a warehouse in a different workspace:

``` yaml
Cross-workspace Warehouse Test:
  source:
    type: fabric_warehouse_spark
    connection: fabric_warehouse_connection
    query: |
      SELECT 
        department,
        COUNT(*) AS employee_count,
        AVG(salary) AS avg_salary
      FROM dbo.employees
      GROUP BY department
  expected:
    type: csv_spark
    path: /lakehouse/default/Files/expected/department_summary.csv
    header: true
    inferSchema: true
```

## Requirements

- Microsoft Fabric environment with active Spark session
- `sempy-labs` package (automatically available in Fabric notebooks)
- Read permissions on the target Fabric Warehouse
- Query permissions on the warehouse tables

## Notes

- The connector operates within an active Spark session in a Fabric environment
- Authentication is automatic when running in a Fabric notebook
- The query executes against the Fabric Warehouse and returns a Spark DataFrame

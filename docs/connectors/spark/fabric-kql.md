# Fabric KQL (Spark)

This connector is used to query Microsoft Fabric KQL databases using Spark and the Kusto Spark connector.

> ⚠️ A Spark connector can only be used with another Spark connector. It is not possible to mix Spark and native connectors in the same test case.

See [Spark mode overview](/docs/spark/overview) for more information.

## Connection configuration

| Name | Mandatory | Default | Description |
|------|:---------:|:-------:|-------------|
| kusto_uri | yes | | Kusto cluster URI (e.g. `https://mycluster.kusto.windows.net`) |
| database_id | yes | | KQL database ID |

### Example

``` yaml
connections:
  kql_connection:
    type: fabric_kql_spark
    kusto_uri: https://mycluster.kusto.windows.net
    database_id: my_kql_database
```

## Test case configuration

| Name | Mandatory | Default | Description |
|------|:---------:|:-------:|-------------|
| query | yes | | KQL query to execute |

### Example

``` yaml
Example Fabric KQL:
  source:
    type: fabric_kql_spark
    connection: kql_connection
    query: |
      Employees
      | where HireDate < datetime(2000-01-01)
      | project EmployeeId, Name, Department, HireDate
  expected:
    type: sql_spark
    query: |
      SELECT *
      FROM expected_employees
      WHERE hire_date < '2000-01-01'
```

## Authentication

This connector uses the Microsoft Fabric authentication token obtained via `mssparkutils.credentials.getToken("kusto")`. The Spark environment must have access to Microsoft Fabric resources.

## Requirements

- Microsoft Kusto Spark connector (`com.microsoft.kusto.spark.datasource`)
- Microsoft Fabric workspace with appropriate permissions
- Spark environment with `mssparkutils` available (typically in Fabric notebooks)

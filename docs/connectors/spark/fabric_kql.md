This connector is used to read data from Microsoft Fabric KQL Database using Spark. 

⚠️ A spark connector can be use only with another spark connector. It is not possible to use a spark connector with a non spark connector.

See [Spark documentation](/docs/configuration-spark-mode/) for more information.

# Connection configuration
| Name              | Mandatory | Default                       | Description |
|-------------------|:---------:|:-----------------------------:|-------------|
| kusto_uri         | yes       |                               | Kusto cluster URI (e.g., https://mycluster.kusto.windows.net)
| database_id       | yes       |                               | KQL Database ID

## Example
``` yaml
connections:
  fabric_kql_connection:
    type: fabric_kql_spark
    kusto_uri: https://mycluster.kusto.windows.net
    database_id: my_database
```

# Configuration
## Test case configuration
| Name              | Mandatory | Default                       | Description |
|-------------------|:---------:|:-----------------------------:|-------------|
| query             | yes       |                               | The KQL query to execute against the database

## Example
``` yaml
Example Fabric KQL Spark:
  source:
    type: fabric_kql_spark
    connection: fabric_kql_connection
    query: |
      Employees
      | where HireDate < datetime(2000-01-01)
      | project EmployeeId, Name, Department, HireDate
  expected:
    type: sql_spark
    query: |
      select * 
      from expected_employees
      where hire_date < "2000-01-01"
```

# Authentication
This connector uses the Microsoft Fabric authentication token obtained via `mssparkutils.credentials.getToken("kusto")`. 
Make sure your Spark environment is properly configured with access to Microsoft Fabric resources.

# Requirements
- Microsoft Kusto Spark connector (`com.microsoft.kusto.spark.datasource`)
- Access to Microsoft Fabric with appropriate permissions
- Spark environment with `mssparkutils` available (typically in Microsoft Fabric notebooks)

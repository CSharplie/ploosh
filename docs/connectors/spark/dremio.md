# Dremio (Spark)

This connector is used to query Dremio using Spark via the Arrow Flight SQL JDBC driver.

> ⚠️ A Spark connector can only be used with another Spark connector. It is not possible to mix Spark and native connectors in the same test case.

See [Spark mode overview](/docs/spark/overview) for more information.

## Connection configuration

| Name | Mandatory | Default | Description |
|------|:---------:|:-------:|-------------|
| host | yes | | Dremio server hostname or IP address |
| port | no | `32010` | Arrow Flight SQL port |
| use_encryption | no | `true` | Enable TLS encryption for the connection |
| disable_certificate_verification | no | `false` | Disable TLS certificate verification (not recommended in production) |
| username | yes | | Dremio username |
| password | yes | | Dremio password or PAT |

### Example

``` yaml
connections:
  dremio_connection:
    type: dremio_spark
    host: my-dremio-server.example.com
    port: 32010
    use_encryption: true
    disable_certificate_verification: false
    username: my_user
    password: $var.dremio_password
```

## Test case configuration

| Name | Mandatory | Default | Description |
|------|:---------:|:-------:|-------------|
| query | yes | | SQL query to execute against Dremio |

### Example

``` yaml
Example Dremio Spark:
  source:
    type: dremio_spark
    connection: dremio_connection
    query: |
      SELECT *
      FROM my_schema.employees
      WHERE hire_date < '2000-01-01'
  expected:
    type: sql_spark
    query: |
      SELECT *
      FROM expected_employees
      WHERE hire_date < '2000-01-01'
```

## Requirements

- Apache Arrow Flight SQL JDBC driver (`org.apache.arrow.driver.jdbc.ArrowFlightJdbcDriver`)
- Dremio instance accessible from the Spark cluster

# Migration testing

Ploosh simplifies testing during data migration projects by allowing you to compare data between legacy and target systems.

## Migration context

In a data migration project (e.g. on-premise to cloud), the key challenge is validating that data feeds produce the **same results** on both platforms. This involves:

- Migrating hundreds of processes/data feeds
- Handling gigabytes of data across many tables
- Ensuring complex calculations and business rules are preserved

## Testing strategy

### Workflow

1. **Code migration**: Develop new processing code for the target environment
2. **Deployment**: Install migrated code on the target platform
3. **Define testing scope**: Identify tables impacted by each feed
4. **Sampling**: Define representative data samples
5. **Write test cases**: Create Ploosh test cases comparing both environments
6. **Execute processes**: Run data feeds on both legacy and target environments
7. **Run tests**: Execute Ploosh to compare samples from both databases
8. **Analysis**: Review results — if a test passes, the feed produces identical results; otherwise, send back for correction

### Connections setup

``` yaml
target_connection:
  type: mysql
  hostname: target-server.database.windows.net
  database: target_db
  username: user
  password: $var.target_password

legacy_connection:
  type: bigquery
  credentials: $var.bq_credentials
  credentials_type: service_account
```

## Sampling strategies

Sampling is crucial for efficient testing. Two main approaches:

### Precise sampling

Select rows using technical or business keys:

``` yaml
Sales migration test:
  options:
    sort:
      - sale_id
  source:
    connection: target_connection
    type: mysql
    query: |
      SELECT *
      FROM fact_sales
      WHERE sale_id IN ('E9EYKDIW6C', 'R5QUFFYXF0', 'FF0YIVG63B',
                         'DZWG6FJQWO', '7Y8G0EQ3JD', '9PF09Z3A6O')
      ORDER BY sale_id
  expected:
    connection: legacy_connection
    type: bigquery
    query: |
      SELECT *
      FROM fact_sales
      WHERE sale_id IN ('E9EYKDIW6C', 'R5QUFFYXF0', 'FF0YIVG63B',
                         'DZWG6FJQWO', '7Y8G0EQ3JD', '9PF09Z3A6O')
      ORDER BY sale_id
```

> Include a large number of values to cover more edge cases.

### Batch sampling

Test a broader set using functional criteria:

``` yaml
Sales migration test:
  options:
    sort:
      - sale_id
  source:
    connection: target_connection
    type: mysql
    query: |
      SELECT *
      FROM fact_sales
      WHERE country = 'france'
      ORDER BY sale_id
  expected:
    connection: legacy_connection
    type: bigquery
    query: |
      SELECT *
      FROM fact_sales
      WHERE country = 'france'
      ORDER BY sale_id
```

> Always add `ORDER BY` clauses for deterministic comparison.

## Useful options for migration

| Option | Use case |
|--------|----------|
| `sort` | Ensure consistent ordering between systems |
| `cast` | Handle type differences between platforms (e.g. INT vs BIGINT) |
| `tolerance` | Allow small numeric differences from floating-point precision |
| `case_insensitive` | Handle case differences in string data |
| `trim` | Handle whitespace differences between systems |
| `ignore` | Exclude columns that are expected to differ (timestamps, audit columns) |

## Tips

- **Sort in queries**: Always add `ORDER BY` in your SQL queries for better performance and deterministic behavior
- **Iterate**: Start with simple tests, then add complexity as you find issues
- **Reuse test cases**: Once a fix is applied, re-run the same test to validate the correction
- **Parameterize**: Use `$var` parameters to switch between environments without modifying test files

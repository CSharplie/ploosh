# Testing approaches

Ploosh is a flexible framework, but the intelligence of the tests lies in the people who write them. This guide presents three key approaches to structuring your data tests.

## By recalculation

This approach validates the results produced by ETL processes by **recalculating the same operations** using independent SQL queries.

### Principle

Write an SQL query that reproduces the calculations and transformations performed by the ETL on a given dataset. Then compare the results of this query to the ETL output. If both match, the test passes.

### Example

Suppose an ETL aggregates sales data by category and region. To verify the results:

``` yaml
Test sales aggregation:
  source:
    connection: dwh
    type: mssql
    query: |
      SELECT category, region, SUM(sales_amount) AS total_sales
      FROM dwh.fact_sales
      GROUP BY category, region

  expected:
    connection: dmt
    type: mssql
    query: |
      SELECT category, region, total_sales
      FROM dmt.fact_sales_aggregated
```

### Use cases

- Verification of complex aggregations (monthly sales by product and region)
- Calculation of ratios or KPIs derived from multiple sources
- Validation of business rules at each stage of data processing

### Trade-offs

The main effort is writing SQL queries that replicate complex transformations. However, it provides fine control and pinpoints exactly where errors occur.

---

## By empty

This approach relies on the **empty** connector for the expected part. The source query should return **no data**. If it does, the test fails.

### Principle

Define a source query whose criteria identify **incorrect or undesirable data**. If the query returns results, it means anomalies exist. If no data is returned, the test passes.

### Example

Check for rejected records inserted in the last 24 hours:

``` yaml
Test no recent rejects:
  source:
    connection: dwh
    type: mssql
    query: |
      SELECT *
      FROM dwh.fact_sales_rejects
      WHERE date_insert BETWEEN DATEADD(day, -1, GETDATE()) AND GETDATE()
  expected:
    type: empty
```

### Use cases

- **Data quality**: Ensure invalid data is not present in target tables
- **Duplicate detection**: Verify no duplicate records exist
- **Consistency checks**: Ensure relationships and business rules are respected
- **NULL checks**: Verify no NULL values in mandatory columns
- **Range validation**: Ensure values fall within expected ranges

### Advantages

- **Simplicity**: Only a source query is needed, no expected query
- **Fast implementation**: Rapid creation of tests for critical checks
- **Flexibility**: Adaptable to many data validation scenarios

---

## By test data

This approach uses **predefined test data** inserted into source systems to simulate specific scenarios.

### Principle

1. Insert known test data into the data sources
2. Run the ETL processes
3. Compare the output against pre-calculated expected results

### Example

Using a CSV file with pre-calculated expected results:

``` yaml
Test transformation rules:
  options:
    sort:
      - employee_id
  source:
    connection: dmt
    type: mysql
    query: |
      SELECT employee_id, full_name, department, is_active
      FROM dmt.dim_employee
      WHERE employee_id IN (9001, 9002, 9003)
  expected:
    type: csv
    path: ./test_data/expected_employees.csv
```

### Use cases

- Validating complex business rules with specific edge cases
- Testing data type conversions and format transformations
- Verifying calculations with known inputs and outputs

### Trade-offs

Requires functional understanding of the system and effort to maintain test datasets. However, it provides the most deterministic and reproducible tests.

---

## Choosing an approach

| Approach | Best for | Complexity | Maintenance |
|----------|----------|------------|-------------|
| **Recalculation** | Aggregations, KPIs, business rules | Medium | Medium |
| **Empty** | Quality checks, duplicates, anomalies | Low | Low |
| **Test data** | Edge cases, transformations, rules | High | High |

In practice, combine all three approaches for comprehensive test coverage.

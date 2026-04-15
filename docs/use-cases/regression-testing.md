# Regression testing

Ploosh can be used as a regression testing framework to ensure that changes to data pipelines do not break existing functionality.

## Context

In data projects, every modification to the ETL chain introduces a risk of regression:

- New feature development
- Bug fixes
- Infrastructure changes
- Dependency updates
- Schema modifications

## Strategy

### Build a test suite incrementally

1. **Start with critical tests**: Focus on the most important tables and business rules
2. **Add tests on bug discovery**: When a bug is found, create a test case that would catch it
3. **Cover all layers**: Test across the entire data chain (raw → warehouse → datamart)

### Example test suite

``` yaml
# Regression test: employee count by department
Test employee count:
  options:
    sort:
      - department
  source:
    connection: dwh
    type: mssql
    query: |
      SELECT department, COUNT(*) AS count
      FROM dwh.dim_employee
      WHERE is_active = 1
      GROUP BY department
  expected:
    connection: dmt
    type: mssql
    query: |
      SELECT department, employee_count AS count
      FROM dmt.department_summary
```

``` yaml
# Regression test: no orphan records
Test no orphan orders:
  source:
    connection: dwh
    type: mssql
    query: |
      SELECT o.order_id
      FROM dwh.fact_orders o
      LEFT JOIN dwh.dim_customer c ON o.customer_id = c.customer_id
      WHERE c.customer_id IS NULL
  expected:
    type: empty
```

## CI/CD integration

Run regression tests automatically after every deployment:

1. Deploy new code to the data platform
2. Execute data pipelines
3. Run Ploosh regression suite
4. Publish results to Azure DevOps / GitHub

See [Azure DevOps pipeline](/docs/pipelines/azure-devops) and [GitHub Actions](/docs/pipelines/github-actions) for integration guides.

## Best practices

- **Version control test cases**: Store YAML files alongside pipeline code in Git
- **Run on every deployment**: Automate execution in CI/CD pipelines
- **Collaborative maintenance**: Tests can be written by developers, testers, and business analysts
- **Use pass_rate for tolerance**: Allow minor acceptable differences instead of strict matching
- **Disable flaky tests**: Use the `disabled` option to temporarily skip unstable tests while investigating

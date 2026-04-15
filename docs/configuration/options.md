# Test case options

Test cases allow defining options to control the comparison behavior. Options are set in the `options` section of the test case YAML.

## All options

| Option | Type | Default | Available in | Description |
|--------|------|:-------:|:------------:|-------------|
| `compare_mode` | string | `order` | Native, Spark | Comparison mode: `order` or `join` |
| `join_keys` | list | `[]` | Spark only | Columns to join on (for `join` mode) |
| `sort` | list | | Native, Spark | Columns to sort before comparison |
| `ignore` | list | | Native, Spark | Columns to exclude from comparison |
| `cast` | list | `[]` | Native, Spark | Columns to cast to a specific type |
| `pass_rate` | decimal | `1` | Native, Spark | Minimum success rate (0.0 to 1.0) |
| `tolerance` | decimal | `0` | Native, Spark | Numeric tolerance for float comparisons |
| `trim` | boolean | `false` | Native, Spark | Trim whitespace from string columns |
| `case_insensitive` | boolean | `false` | Native, Spark | Convert strings to lowercase before comparing |
| `allow_no_rows` | boolean | `true` | Native, Spark | Allow both datasets to be empty without error |
| `disabled` | boolean | `false` | Native, Spark | Skip this test case entirely |

---

## compare_mode

Defines how rows are matched between source and expected datasets.

| Mode | Description | Available in |
|------|-------------|:------------:|
| `order` | Rows are matched by position (row 1 vs row 1, row 2 vs row 2, etc.) | Native, Spark |
| `join` | Rows are matched by joining on `join_keys` columns | Spark only |

### Example (order mode — default)

``` yaml
Example:
  options:
    compare_mode: order
    sort:
      - employee_id
  source:
    type: sql_spark
    query: SELECT * FROM employees ORDER BY employee_id
  expected:
    type: csv_spark
    path: ./expected.csv
```

### Example (join mode — Spark only)

``` yaml
Example:
  options:
    compare_mode: join
    join_keys:
      - employee_id
  source:
    type: sql_spark
    query: SELECT * FROM employees
  expected:
    type: csv_spark
    path: ./expected.csv
```

> The `join` mode is useful when row ordering is non-deterministic or when matching by business keys is more appropriate.

---

## sort

Sort both datasets before comparison. Specify a list of column names to sort by, or `["*"]` to sort by all columns.

``` yaml
Example:
  options:
    sort:
      - department
      - name
  source:
    type: mysql
    connection: my_connection
    query: SELECT * FROM employees
  expected:
    type: csv
    path: ./expected.csv
```

> **Best practice**: Sort in your SQL queries (`ORDER BY`) for better performance and deterministic results.

---

## ignore

Exclude specific columns from the comparison. Useful for audit columns, timestamps, or auto-generated fields.

``` yaml
Example:
  options:
    ignore:
      - created_at
      - updated_at
  source:
    type: mysql
    connection: my_connection
    query: SELECT * FROM employees
  expected:
    type: csv
    path: ./expected.csv
```

---

## cast

Cast column types before comparison. Useful when source and expected have different types for the same data.

Allowed types: `int`, `float`, `string`, `datetime`

``` yaml
Example:
  options:
    cast:
      - name: salary
        type: float
      - name: hire_date
        type: datetime
  source:
    type: mysql
    connection: my_connection
    query: SELECT * FROM employees
  expected:
    type: csv
    path: ./expected.csv
```

---

## pass_rate

Define the minimum percentage of matching rows required for the test to pass. Value between `0.0` and `1.0` (default: `1.0` = all rows must match).

``` yaml
Example:
  options:
    pass_rate: 0.95
  source:
    type: mysql
    connection: my_connection
    query: SELECT * FROM employees
  expected:
    type: csv
    path: ./expected.csv
```

> A `pass_rate` of `0.95` means the test passes if at least 95% of rows match.

---

## tolerance

Allow small numeric differences when comparing float/decimal columns. Set to `0` (default) for exact matching.

``` yaml
Example:
  options:
    tolerance: 0.01
  source:
    type: mysql
    connection: my_connection
    query: SELECT * FROM financial_data
  expected:
    type: csv
    path: ./expected.csv
```

> Useful for floating-point precision differences between systems (e.g. migration from one database to another).

---

## trim

Trim leading and trailing whitespace from all string columns before comparison.

``` yaml
Example:
  options:
    trim: true
  source:
    type: mysql
    connection: my_connection
    query: SELECT * FROM employees
  expected:
    type: csv
    path: ./expected.csv
```

---

## case_insensitive

Convert all string values to lowercase before comparison.

``` yaml
Example:
  options:
    case_insensitive: true
  source:
    type: mysql
    connection: my_connection
    query: SELECT * FROM employees
  expected:
    type: csv
    path: ./expected.csv
```

---

## allow_no_rows

When set to `true` (default), the test passes if both source and expected datasets are empty. When `false`, empty datasets cause the test to fail.

``` yaml
Example:
  options:
    allow_no_rows: false
  source:
    type: mysql
    connection: my_connection
    query: SELECT * FROM employees WHERE department = 'NonExistent'
  expected:
    type: empty
```

---

## disabled

Skip a test case entirely. The test will appear as `notExecuted` in the results.

``` yaml
Temporarily disabled test:
  disabled: true
  source:
    type: mysql
    connection: my_connection
    query: SELECT * FROM problematic_table
  expected:
    type: empty
```

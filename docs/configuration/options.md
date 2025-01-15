Test case allow to define options for the test case execution. The options are defined in the `options` section of the test case configuration.

# Ignore
The `ignore` option allow to ignore specifics columns in the comparison. The `ignore` option is a list of columns to ignore in the comparison. The columns are defined by their name.

## Example
``` yaml
Example:
  options:
    ignore:
      - column_to_ignore_1
      - column_to_ignore_2
  source:
    connection: my_connection
    query: select * from my_table
  expected:
    connection: my_connection
    query: select * from my_table
```

# Sort
The `sort` option allow to sort the dataset before the comparison. The `sort` option is a list of columns to sort the dataset. The columns are defined by their name.

## Example
``` yaml
Example:
  options:
    sort:
      - column_to_sort_1
      - column_to_sort_2
  source:
    connection: my_connection
    query: select * from my_table
  expected:
    connection: my_connection
    query: select * from my_table
```

⚠️ The best practice is to sort the dataset in the source and the expected query to ensure the comparison is done on the same order and provide a better performance.

# Cast
The `cast` option allow to cast the column type before the comparison. The `cast` option is a list of name and type to cast the column. The column name is defined by their name and the type.

The allowed types are:
- `int`
- `float`
- `string`
- `datetime`

## Example
``` yaml
Example:
  options:
    cast:
      - name: column_to_cast_1
        type: int
    - name: column_to_cast_2
        type: float
    source:
        connection: my_connection
        query: select * from my_table
    expected:
        connection: my_connection
        query: select * from my_table
```

# Pass rate
The `pass_rate` option allow to define the pass rate of the test case. The pass rate is a float between 0 and 1. The pass rate is the percentage of the rows that need to be the same to pass the test case.

## Example
``` yaml
Example:
  options:
    pass_rate: 0.95
  source:
    connection: my_connection
    query: select * from my_table
  expected:
    connection: my_connection
    query: select * from my_table
```

# Trim
The `trim` option allow to trim the string columns before the comparison. The `trim` option is a list of columns to trim. The columns are defined by their name.

## Example
``` yaml
Example:
  options:
    trim:
      - column_to_trim_1
      - column_to_trim_2
  source:
    connection: my_connection
    query: select * from my_table
  expected:
    connection: my_connection
    query: select * from my_table
```

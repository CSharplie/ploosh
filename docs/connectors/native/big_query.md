This connector allows you to connect to a bigquery instance and execute SQL queries.

# Connection configuration
## Definition
| Name                     | Mandatory | Default    | Description |
|--------------------------|:---------:|:----------:|-------------|
| credentials              | yes       |            | The authentication use a [google keyfile](https://googleapis.dev/python/google-api-core/latest/auth.html) encoded in base 64

⚠️ it's highly recommended to use a [parameter](/docs/configuration-custom-parameters/) to pass the credentials value

## Example
``` yaml
bigquery_example:
  type: bigquery
  credentials: $var.gbq_sample_token
```

# Test case configuration
## Definition
| Name              | Mandatory | Default                       | Description |
|-------------------|:---------:|:-----------------------------:|-------------|
| connection        | yes       |                               | The connection to use 
| query             | yes       |                               | The query to execute to the database

## Example
``` yaml
Example BigQuery:
  source:
    connection: bigquery_example
    type: bigquery
    query: | 
        select * 
            from `rh.employees`
            where hire_date < "2000-01-01"
  expected:
    type: csv
    path: data/employees_before_2000.csv
```
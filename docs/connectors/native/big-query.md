# BigQuery

This connector is used to query Google BigQuery using SQL.

## Connection configuration

| Name | Mandatory | Default | Description |
|------|:---------:|:-------:|-------------|
| credentials_type | no | `service_account` | Authentication type: `service_account` or `current_user` |
| credentials | no | | Google [keyfile](https://googleapis.dev/python/google-api-core/latest/auth.html) encoded in base64 (for `service_account` mode) |
| project_id | no | | Google Cloud project ID (for `current_user` mode) |

When `credentials_type` is `service_account`, the `credentials` parameter must contain a base64-encoded Google service account keyfile.

When `credentials_type` is `current_user`, the connector uses `pandas_gbq` with the default credentials from the environment (e.g. gcloud CLI or the `GOOGLE_APPLICATION_CREDENTIALS` environment variable).

> ⚠️ It is highly recommended to use a [custom parameter](/docs/configuration/custom-parameters) to pass the credentials value.

### Example

``` yaml
connections:
  bigquery_example:
    type: bigquery
    credentials_type: service_account
    credentials: $var.gbq_credentials
```

## Test case configuration

| Name | Mandatory | Default | Description |
|------|:---------:|:-------:|-------------|
| query | yes | | SQL query to execute |

### Example

``` yaml
Example BigQuery:
  source:
    type: bigquery
    connection: bigquery_example
    query: |
      SELECT *
      FROM `rh.employees`
      WHERE hire_date < "2000-01-01"
  expected:
    type: csv
    path: data/employees_before_2000.csv
```

## Requirements

- `pip install pandas-gbq` (included in `ploosh` full installation)
- For `service_account` mode: a valid Google Cloud service account keyfile
```
# Semantic Model (XMLA)

This connector is used to query Microsoft Fabric Semantic Models (Power BI datasets) using the XMLA endpoint REST API with DAX queries.

## Connection configuration

| Name | Mandatory | Default | Description |
|------|:---------:|:-------:|-------------|
| mode | no | `oauth` | Authentication mode: `oauth` |
| dataset_id | yes | | Power BI dataset ID |
| token | no | | Access token (for `token` mode) |
| tenant_id | no | | Azure AD tenant ID (for `spn` mode) |
| client_id | no | | Azure AD application client ID (for `spn` mode) |
| client_secret | no | | Azure AD application client secret (for `spn` mode) |

### Authentication modes

| Mode | Description |
|------|-------------|
| `oauth` | Opens a browser login page for interactive authentication |

## Connection example

``` yaml
connections:
  my_semantic_model:
    type: semantic_model
    mode: oauth
    dataset_id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

## Test case configuration

| Name | Mandatory | Default | Description |
|------|:---------:|:-------:|-------------|
| query | yes | | DAX query to execute |
| body | no | | Custom request body (overrides default) |

## Test case example

``` yaml
Test semantic model measure:
  source:
    type: semantic_model
    connection: my_semantic_model
    query: |
      EVALUATE
      SUMMARIZECOLUMNS(
        DimDate[Year],
        "Revenue", [Total Revenue]
      )
  expected:
    type: csv
    path: ./expected/revenue_by_year.csv
```

## How it works

The connector sends a POST request to the Power BI REST API:

```
POST https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}/executeQueries
```

The DAX query is wrapped in a JSON body with `includeNulls: true` and the results are parsed into a DataFrame.

## Requirements

- `pip install azure-identity requests`
- Power BI Premium or Fabric capacity (XMLA endpoint must be enabled)
- Appropriate permissions on the dataset

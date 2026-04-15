# Analysis Services

This connector is used to query Analysis Services models using DAX queries via the ADOMD.NET library.

> This connector requires Windows and the ADOMD.NET library (`pyadomd` + `pythonnet`).

## Connection configuration

| Name | Mandatory | Default | Description |
|------|:---------:|:-------:|-------------|
| mode | no | `oauth` | Authentication mode: `oauth`, `pbix` |
| server | yes | | Analysis Services server address |
| dataset_id | yes | | Dataset ID (in DAX Studio: right-click model name → "Copy Database ID") |
| token | no | | Access token (for `token` mode) |
| username | no | | Username (for `credentials` mode) |
| password | no | | Password (for `credentials` mode) |
| tenant_id | no | | Azure AD tenant ID (for `spn` mode) |
| client_id | no | | Azure AD application client ID (for `spn` mode) |
| client_secret | no | | Azure AD application client secret (for `spn` mode) |
| scope | no | `https://analysis.windows.net/powerbi/api/.default` | OAuth scope |

### Authentication modes

| Mode | Description |
|------|-------------|
| `oauth` | Opens a browser login page. Auto-connects for local AS instances |
| `pbix` | Same as `oauth`, used for local Power BI Desktop models |

## Connection example

``` yaml
connections:
  my_analysis_services:
    type: analysis_services
    mode: oauth
    server: powerbi://api.powerbi.com/v1.0/myorg/MyWorkspace
    dataset_id: my-dataset-id
```

## Test case configuration

| Name | Mandatory | Default | Description |
|------|:---------:|:-------:|-------------|
| query | yes | | DAX query to execute |

## Test case example

``` yaml
Test DAX measure:
  source:
    type: analysis_services
    connection: my_analysis_services
    query: |
      EVALUATE
      SUMMARIZECOLUMNS(
        DimProduct[Category],
        "Total Sales", [Total Sales]
      )
  expected:
    type: csv
    path: ./expected/sales_by_category.csv
```

## Requirements

- Windows OS
- ADOMD.NET library installed (typically at `C:\Program Files\Microsoft.NET\ADOMD.NET\`)
- `pip install pyadomd pythonnet`
- For `spn` mode: `pip install azure-identity`

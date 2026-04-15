# Python API — execute_cases()

The `execute_cases()` function is the main entry point for running Ploosh programmatically from Python, typically in notebooks (Microsoft Fabric, Databricks) or custom scripts.

## Import

``` python
from ploosh import execute_cases
```

## Signature

``` python
execute_cases(
    cases=None,
    connections=None,
    spark=None,
    spark_session=None,
    filter=None,
    path_output=None,
    variables=None,
)
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|:-------:|-------------|
| `cases` | string | | Path to the folder containing test case YAML files |
| `connections` | string | | Path to the connections YAML file |
| `spark` | string | | Set to `"true"` to enable Spark mode |
| `spark_session` | SparkSession | | Existing PySpark SparkSession to use |
| `filter` | string | | Glob pattern to filter test case files (e.g. `"*.yaml"`) |
| `path_output` | string | | Path to the output folder for results |
| `variables` | dict | | Dictionary of custom parameter values |

## Examples

### Basic usage

``` python
from ploosh import execute_cases

execute_cases(
    cases="test_cases",
    connections="connections.yml"
)
```

### Microsoft Fabric

``` python
from ploosh import execute_cases

execute_cases(
    cases="/lakehouse/default/Files/ploosh_cases",
    connections="/lakehouse/default/Files/ploosh_connections.yaml",
    spark_session=spark,
    path_output="/lakehouse/default/Files/ploosh_outputs"
)
```

### Databricks

``` python
from ploosh import execute_cases

execute_cases(
    cases="/Workspace/Shared/cases",
    connections="/Workspace/Shared/connections.yaml",
    spark_session=spark,
    path_output="/Workspace/Shared/output"
)
```

### With variables

``` python
from ploosh import execute_cases

execute_cases(
    cases="test_cases",
    connections="connections.yml",
    variables={
        "db_password": "my_secret",
        "schema": "production"
    }
)
```

### With filter

``` python
from ploosh import execute_cases

execute_cases(
    cases="test_cases",
    connections="connections.yml",
    filter="quality_*.yaml"
)
```

## Behavior

- If `spark_session` is provided, Ploosh uses it for Spark connectors
- If `spark="true"` and no `spark_session` is given, Ploosh creates a local SparkSession
- Results are exported to `{path_output}/{format}/` (e.g. `output/json/test_results.json`)
- The function prints status to stdout in real-time
- By default, raises `SystemExit(1)` if any test fails. Use `--failure false` from CLI or handle the exit in your code

# Command line

Ploosh can be executed from the command line using the `ploosh` command.

## Usage

``` shell
ploosh --connections <path> --cases <path> [options]
```

## Arguments

| Argument | Mandatory | Default | Description |
|----------|:---------:|:-------:|-------------|
| `--connections` | no | | Path to the connections YAML file |
| `--cases` | no | `./cases` | Path to the folder containing test case YAML files |
| `--filter` | no | `*.yml` | Glob pattern to filter test case files |
| `--output` | no | `./output` | Path to the output folder for results |
| `--export` | no | `JSON` | Export format: `JSON`, `CSV`, or `TRX` |
| `--spark` | no | `false` | Enable Spark mode (creates a local SparkSession) |
| `--failure` | no | `true` | Exit with code 1 if any test fails or errors |
| `--p_<name>` | no | | Custom parameter value (see [Custom parameters](/docs/configuration/custom-parameters)) |

## Examples

### Basic execution

``` shell
ploosh --connections "connections.yml" --cases "test_cases"
```

### With export format and parameters

``` shell
ploosh --connections "connections.yml" --cases "test_cases" --export "TRX" --p_db_password "my_password"
```

### With filter and custom output

``` shell
ploosh --connections "connections.yml" --cases "test_cases" --filter "*.yaml" --output "./results"
```

### Disable failure exit code

Useful in CI/CD pipelines where you want to publish results even when tests fail:

``` shell
ploosh --connections "connections.yml" --cases "test_cases" --failure false
```

### Spark mode

``` shell
ploosh --connections "connections.yml" --cases "test_cases" --spark true
```

> When `--spark true` is set and no spark session is provided programmatically, Ploosh creates a local SparkSession. For Fabric or Databricks, use the Python API instead. See [Spark mode overview](/docs/spark/overview).

## Python API

When running inside a notebook (Fabric, Databricks), use the `execute_cases()` function instead:

``` python
from ploosh import execute_cases

execute_cases(
    cases="/path/to/cases",
    connections="/path/to/connections.yaml",
    spark_session=spark
)
```

See [Python API reference](/docs/api/execute-cases) for all parameters.

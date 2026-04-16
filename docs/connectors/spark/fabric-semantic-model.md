# Fabric Semantic Model Spark connector

This connector is used to query a Microsoft Fabric Semantic Model and return a Spark DataFrame.

Warning: a Spark connector can be used only with another Spark connector. It is not possible to use a Spark connector with a non-Spark connector.

See [Spark documentation](Spark) for more information.

# Connection configuration

| Name | Mandatory | Default | Description |
|------|:---------:|:-------:|-------------|
| semantic_model_name | yes |  | Semantic model (dataset) name in Fabric |
| workspace_name | no | `null` | Fabric workspace name. If omitted, default workspace context is used |

# Configuration

## Test case configuration

| Name | Mandatory | Default | Description |
|------|:---------:|:-------:|-------------|
| method | yes |  | Query method. Allowed values: `DAX Query`, `Table`, `Measure` |
| dax_query | no | `null` | DAX query text. Used when `method: DAX Query` |
| table_to_query | no | `null` | Table name to read. Used when `method: Table` |
| measure_to_query | no | `null` | Measure name to evaluate. Used when `method: Measure` |
| group_by | no | `null` | List of grouping columns for measure evaluation. Used when `method: Measure` |
| filters_to_apply | no | `null` | Dictionary of filters for measure evaluation. Used when `method: Measure` |
| column_names | yes |  | List of output column names. List size must match returned column count |


## Examples

```yaml
Example Fabric Semantic Model DAX:
  source:
    type: fabric_semantic_model_spark
    connection: test_fabric_semantic_model_spark
    method: DAX Query
    dax_query: |
      EVALUATE SUMMARIZECOLUMNS(
        'CountrySales'[Country],
        'CountrySales'[Sales]
      )
    column_names:
      - Country
      - Sales
  expected:
    type: empty_spark
```

```yaml
Example Fabric Semantic Model Measure:
  source:
    type: fabric_semantic_model_spark
    connection: test_fabric_semantic_model_spark
    method: Measure
    measure_to_query: Sales with tax
    group_by:
      - "'CountrySales'[Country]"
    filters_to_apply:
      {"'CountrySales'[Country]" : ["France", "Germany"]}
  expected:
    type: empty_spark
```

```yaml
Example Fabric Semantic Model Table:
  source:
    type: fabric_semantic_model_spark
    connection: test_fabric_semantic_model_spark
    method: Table
    table_to_query: CountrySales
    column_names:
      - Country
      - Sales
  expected:
    type: empty_spark
```

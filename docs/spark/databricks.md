# Databricks setup

This guide explains how to run Ploosh on Databricks using Spark mode.

## Step 1: Install Ploosh

In the first cell of your Databricks notebook:

``` python
%pip install ploosh
```

## Step 2: Restart Python

Databricks requires a Python restart after installing new packages:

``` python
dbutils.library.restartPython()
```

## Step 3: Execute Ploosh

``` python
from ploosh import execute_cases

root_folder = "/Workspace/Shared"

execute_cases(
    cases=f"{root_folder}/cases",
    connections=f"{root_folder}/connections.yaml",
    spark_session=spark,
    path_output=f"{root_folder}/output"
)
```

## File organization

Organize your files in the Databricks workspace:

```
/Workspace/Shared/
├── connections.yaml        → Connection definitions
├── cases/                  → Test case YAML files
│   ├── validation.yaml
│   └── quality_checks.yaml
└── output/                 → Generated results
    └── json/
        ├── test_results.json
        └── test_results/
            └── *.xlsx
```

## Using Unity Catalog

When using Databricks Unity Catalog, you can query tables directly with the `sql_spark` connector:

``` yaml
Test catalog data:
  source:
    type: sql_spark
    query: |
      SELECT *
      FROM my_catalog.my_schema.employees
      WHERE department = 'Engineering'
  expected:
    type: csv_spark
    path: /Workspace/Shared/expected/employees.csv
```

## Using variables

Pass variables to Ploosh for dynamic configuration:

``` python
execute_cases(
    cases=f"{root_folder}/cases",
    connections=f"{root_folder}/connections.yaml",
    spark_session=spark,
    variables={
        "env": "production",
        "db_password": dbutils.secrets.get("my-scope", "db-password")
    }
)
```

## Scheduling

Use Databricks **Jobs** to schedule Ploosh execution:

1. Create a new Job
2. Add a Notebook task pointing to your Ploosh notebook
3. Configure schedule (cron, trigger, or manual)
4. Optionally add parameters to override notebook widgets

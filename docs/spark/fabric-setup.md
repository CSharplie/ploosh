# Microsoft Fabric setup

This guide details how to set up Ploosh in a Microsoft Fabric environment to validate your data platform workloads.

## Architecture overview

The recommended architecture is based on a **dedicated Fabric workspace** structured as follows:

```
Ploosh Workspace
├── Python Environment     → Ploosh package pre-installed
├── Lakehouse
│   ├── Files/
│   │   ├── ploosh_cases/         → Test case definitions (YAML)
│   │   ├── ploosh_connections.yaml → Connection definitions
│   │   ├── ploosh_resources/     → Reference datasets (CSV, Parquet, etc.)
│   │   └── ploosh_outputs/       → Test results (JSON, XLSX)
│   ├── Tables/
│   │   └── ploosh_results        → Results history (Delta table)
│   └── Shortcuts/                → Links to other workspace Lakehouses
├── Notebook                → Orchestration notebook
├── Semantic Model          → Results exposure for analysis
└── Power BI Report         → Quality dashboard
```

## Step 1: Create the Python environment

1. In your Fabric workspace, create a new **Environment**
2. In the environment settings, add `ploosh` as a pip package
3. Save and publish the environment

This ensures Ploosh is available by default in all notebooks using this environment.

## Step 2: Create the Lakehouse

Create a Lakehouse named (e.g. `ploosh_lakehouse`) and organize the `Files/` folder:

| Folder | Purpose |
|--------|---------|
| `ploosh_cases/` | Test case YAML files |
| `ploosh_resources/` | Reference data files (CSV, JSON, Parquet) used in expected tests |
| `ploosh_outputs/` | Output folder for test results |

Upload your `ploosh_connections.yaml` file to `Files/`.

## Step 3: Configure shortcuts

To access data located in other Fabric workspaces, use **shortcuts**:

1. In the Lakehouse, go to the **Tables** section
2. Click **New shortcut**
3. Select the source (OneLake, Azure Data Lake, etc.)
4. Map the target Lakehouse tables from other workspaces

This makes remote tables queryable via Spark SQL as if they were local.

See [Shortcuts strategy](/docs/spark/fabric-shortcuts) for more details.

## Step 4: Create the connections file

Create a `ploosh_connections.yaml` file for your Fabric data sources:

``` yaml
# For KQL databases
kql_connection:
  type: fabric_kql_spark
  kusto_uri: https://mycluster.kusto.windows.net
  database_id: my_kql_database

# No connection needed for Spark SQL (uses shortcuts)
```

> Spark SQL queries against Lakehouse tables via shortcuts do not require a connection definition. Use the `sql_spark` connector directly.

## Step 5: Create test cases

Create YAML files in `ploosh_cases/`:

``` yaml
Test employee count:
  source:
    type: sql_spark
    query: |
      SELECT department, COUNT(*) AS employee_count
      FROM hr_lakehouse.employees
      GROUP BY department
  expected:
    type: sql_spark
    query: |
      SELECT department, expected_count AS employee_count
      FROM ploosh_resources.expected_employee_counts

Test no KQL anomalies:
  source:
    type: fabric_kql_spark
    connection: kql_connection
    query: |
      AnomalyEvents
      | where Timestamp > ago(1d)
      | where Severity == "Critical"
  expected:
    type: empty_spark
```

## Step 6: Create the orchestration notebook

See [Fabric notebook orchestration](/docs/spark/fabric-notebook) for a complete notebook implementation.

## Step 7: Schedule execution

You can automate test execution through:

- **Fabric Pipeline**: Add a Notebook activity pointing to the orchestration notebook
- **Schedule**: Configure a recurring schedule on the notebook directly
- **Event trigger**: Trigger tests after upstream pipeline completion

See [Fabric pipeline integration](/docs/pipelines/fabric-pipeline) for pipeline examples.

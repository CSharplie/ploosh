# Fabric Pipeline

Ploosh can be orchestrated directly from a Microsoft Fabric Pipeline using a Notebook activity.

## Pipeline setup

### Step 1: Create the orchestration notebook

Follow the [Fabric notebook guide](/docs/spark/fabric-notebook) to create a notebook with parameterized execution.

### Step 2: Create the pipeline

1. In your Fabric workspace, click **New** → **Data pipeline**
2. Add a **Notebook** activity
3. Configure the activity:
   - **Notebook**: Select the Ploosh orchestration notebook
   - **Base parameters**: Override `cases_sub_folder` and `cases_filter` as needed

### Step 3: Parameterize the pipeline

You can pass parameters to the notebook to target specific test suites:

| Parameter | Type | Example | Description |
|-----------|------|---------|-------------|
| `cases_sub_folder` | string | `/daily_checks` | Subfolder within `ploosh_cases/` |
| `cases_filter` | string | `*.yaml` | Glob pattern for test case files |

### Step 4: Add upstream activities

Chain the Ploosh notebook after your data pipeline activities:

```
[Ingest Data] → [Transform Data] → [Run Ploosh Tests] → [Send Notification]
```

## Example pipeline structure

``` json
{
  "activities": [
    {
      "name": "Run Data Pipeline",
      "type": "Pipeline",
      "dependsOn": []
    },
    {
      "name": "Run Ploosh Tests",
      "type": "Notebook",
      "dependsOn": [
        {
          "activity": "Run Data Pipeline",
          "dependencyConditions": ["Succeeded"]
        }
      ],
      "parameters": {
        "cases_sub_folder": "/",
        "cases_filter": "*.yaml"
      }
    }
  ]
}
```

## Scheduling

Configure the pipeline trigger:

- **Schedule**: Daily, hourly, or custom cron
- **Event-based**: After another pipeline completes
- **Manual**: On-demand execution

## Monitoring

After execution:

1. Check the pipeline run status in Fabric
2. Review detailed results in the `ploosh_results` Delta table
3. Open the Power BI report for visual quality dashboard

See [Fabric reporting](/docs/spark/fabric-reporting) for dashboard setup.

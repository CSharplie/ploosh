Ploosh can be executed over spark (in Databricks, Microsoft Fabric or local)) using spark connectors and by calling from python code.

1. **Manual Spark session**: Pass an existing Spark session manually via the `spark_session` parameter.
2. **Custom Spark session from YAML configuration**: You can specify a custom Spark session configuration using a YAML file. Ploosh will create a dedicated session based on the configuration when the connector name matches the YAML key.
3. **Default Spark session**: If no Spark session is provided and no YAML configuration matches, Ploosh will automatically create a default local Spark session — but only if `spark=True` is passed to `execute_cases`.


# Examples

### Microsoft Fabric

__Cell 1__ : Install Ploosh package from PyPi package manager
``` shell
pip install ploosh
```

__Cell 2__ : Mount the lakehouse to acces the case and connection files
``` python
mount_point = "/ploosh_config"
workspace_name = "ploosh"
lakehouse_name = "data"

if(mssparkutils.fs.mount(f"abfss://{workspace_name}@onelake.dfs.fabric.microsoft.com/{lakehouse_name}.Lakehouse/", mount_point)):
    ploosh_config_path =  mssparkutils.fs.getMountPath(mountPoint = mount_point)
```

__Cell 3__ : Execute ploosh framework
``` python
from ploosh import execute_cases

connections_file_path = f"{ploosh_config_path}/Files/connections.yaml"
cases_folder_path = f"{ploosh_config_path}/Files/cases"

execute_cases(cases = cases_folder_path, connections = connections_file_path, spark_session = spark)
```

## Databricks

__Cell 1__ : Install Ploosh package from PyPi package manager
``` shell
%pip install ploosh
```

__Cell 2__ : Restart python to make the package available
``` python
dbutils.library.restartPython()
```

__Cell 3__ : Execute ploosh framework
``` python
from ploosh import execute_cases

root_folder = "/Workspace/Shared"

execute_cases(cases=f"{root_folder}/cases", path_output=f"{root_folder}/output", spark_session=spark)
```

## Local

__Step 1__ : Install Ploosh package from PyPi package manager
``` shell
pip install ploosh
```

__Step 2__ : Initialize the spark session
``` python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("Ploosh").getOrCreate()
```

__Step 3__ : Execute ploosh framework
``` python
from ploosh import execute_cases

execute_cases(cases = "test_cases", connections = "connections.yml", spark_session = spark)
```

## YAML-based Spark Configuration (optional)

Ploosh allows, also, defining custom Spark sessions for each connector using YAML files. This avoids passing a Spark session manually.

__Step 1__ : Create a YAML file with your configuration
```yaml
DELTA_SPARK:
  spark.master: spark://localhost:7077
  spark.jars.packages: /path/to/delta-spark_2.12-3.2.0.jar
```

> 💡 The top-level key (e.g. `DELTA_SPARK`) must match the connector name defined in your connections.yml file.

__Step 2__ : Call `execute_cases` with the new parameters

```python
from ploosh import execute_cases

execute_cases(
    cases="test_cases",
    connections="connections.yml",
    spark_configuration_path="path/to/spark/configs",
    spark_configuration_filter="*.yml"
)
```

✅ If a connector name matches a key in the YAML configuration, Ploosh will create a dedicated Spark session using the specified settings.

❌ If there is no match and the connector is Spark-enabled (i.e., the `spark` parameter is `True`), the connector will fall back to the default Spark session (either provided manually with `spark_session=` or created locally).


## Default Spark Session (no manual or YAML configuration)

If you don’t pass a Spark session manually and don’t provide a YAML configuration, Ploosh will automatically create a default Spark session — but only if `spark=True` is passed to `execute_cases`.

__Step 1__ : Example `connections.yml` with a Spark-enabled connector
```yaml
MY_SPARK_CONNECTOR:  
  source:
    type: CSV_SPARK
    path: "../path/to/csv/data.csv"
    delimiter: ","

  expected:
    type: CSV_SPARK
    path: "../path/to/csv/data_target.csv"
    delimiter: ","
  ...

__Step 2__ : Run without manually creating or passing a Spark session

```python
from ploosh import execute_cases

execute_cases(
    cases = "test_cases",
    connections = "connections.yml",
    spark = True
)
```
✅ Since `spark=True` is passed to `execute_cases`, Ploosh will automatically create a default Spark session and assign it to the connector.
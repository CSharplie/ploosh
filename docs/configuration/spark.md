Ploosh can be executed over spark (in Databricks, Microsoft Fabric or local)) using spark connectors and by calling from python code.

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


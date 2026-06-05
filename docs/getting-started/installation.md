# Installation

## Requirements

- Python 3.9 or higher

## Install from PyPi

Ploosh is available on [PyPi](https://pypi.org/project/ploosh/) and can be installed using pip.

### Core installation

By default, `ploosh` installs a lightweight core with the native (pandas-based) engine and file connectors only:

``` shell
pip install ploosh
```

### Optional connectors (extras)

Connector-specific dependencies are provided as optional extras. Install only what you need:

``` shell
pip install "ploosh[mysql]"              # MySQL
pip install "ploosh[postgresql]"         # PostgreSQL
pip install "ploosh[snowflake,bigquery]" # multiple extras at once
```

Available extras:

| Extra | Connector / Feature | Main dependency |
|-------|---------------------|-----------------|
| `spark` | Spark engine and Spark connectors | `pyspark`, `delta-spark` |
| `mysql` | MySQL | `pymysql` |
| `postgresql` | PostgreSQL | `pg8000` |
| `sqlserver` | SQL Server | `pyodbc` |
| `odbc` | ODBC | `pyodbc` |
| `snowflake` | Snowflake | `snowflake-sqlalchemy` |
| `databricks` | Databricks | `databricks-sql-connector` |
| `bigquery` | BigQuery | `pandas-gbq`, `sqlalchemy-bigquery` |
| `xmla` | Analysis Services, Semantic Model (XMLA) | `pyadomd`, `azure-identity` |
| `fabric` | Fabric semantic model / warehouse | `semantic-link-labs` |

### Full installation

Includes every connector (all extras above):

``` shell
pip install "ploosh[full]"
```

## Install for Spark mode

The Spark engine is **not** included in the core installation. Install the `spark` extra to enable it:

``` shell
pip install "ploosh[spark]"
```

When running Ploosh inside a managed Spark environment (Microsoft Fabric, Databricks) that already provides PySpark, install the package directly in the notebook:

``` python
%pip install ploosh
```

See [Spark documentation](/docs/spark/overview) for detailed setup instructions.

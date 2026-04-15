# Installation

## Requirements

- Python 3.8 or higher

## Install from PyPi

Ploosh is available on [PyPi](https://pypi.org/project/ploosh/) and can be installed using pip.

### Full installation

Includes all connectors (databases, cloud platforms, BI tools):

``` shell
pip install ploosh
```

### Core installation

Includes only the core connectors (files, empty) with minimal dependencies:

``` shell
pip install ploosh-core
```

### Dependencies

The full installation includes the following additional packages for database and cloud connectors:

| Package | Connector |
|---------|-----------|
| `pyodbc` | SQL Server, ODBC |
| `pymysql` | MySQL |
| `pg8000` | PostgreSQL |
| `snowflake-sqlalchemy` | Snowflake |
| `databricks-sqlalchemy` | Databricks |
| `pandas-gbq` | BigQuery |
| `azure-identity` | Analysis Services, Semantic Model |
| `pyadomd` | Analysis Services |

## Install for Spark mode

When running Ploosh inside a Spark environment (Microsoft Fabric, Databricks), install the package directly in the notebook:

``` python
%pip install ploosh
```

See [Spark documentation](/docs/spark/overview) for detailed setup instructions.

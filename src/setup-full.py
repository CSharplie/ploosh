from setup import setup_ploosh

install_requires = [
    "pyodbc==5.0.1",
    "pymysql==1.1.0",
    "pg8000==1.30.3",
    "snowflake-sqlalchemy==1.5.1",
    "databricks-sql-connector==2.9.3",
    "sqlalchemy-bigquery==1.9.0",
    "google-cloud-bigquery-storage==2.24.0",
    "pandas-gbq==0.23.0",
    "pydata-google-auth==1.8.2"
]

setup_ploosh("ploosh", install_requires)

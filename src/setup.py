"""Setup PyPi module"""
from setuptools import setup, find_packages

setup (
    name = "ploosh",
    version = "0.1.0",
    platforms="Any",
    long_description="tests",
    python_requires=">=3.6",
    license= "Apache License 2.0",
    packages = find_packages(),
    entry_points = {
        "console_scripts": [
            "ploosh = ATF.__main__:main"
        ]
    },
    install_requires=[
        "colorama==0.4.6",
        "PyYAML==6.0.1",
        "Pyjeb==0.2.1",
        "pandas==2.1.4",
        "openpyxl==3.1.2",
        "sqlalchemy==1.4.51",
        "pyodbc==5.0.1",
        "pymysql==1.1.0",
        "pg8000==1.30.3",
        "snowflake-sqlalchemy==1.5.1",
        "databricks-sql-connector==2.9.3",
        "sqlalchemy-bigquery==1.9.0",
        "google-cloud-bigquery-storage==2.24.0",
    ],
)

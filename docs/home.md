# What is Ploosh?

Ploosh is yaml based framework used to automatize the testing process in data projects. It is designed to be simple to use and to be easily integrated in any CI/CD pipelines and it is also designed to be easily extended to support new data connectors.

## Connectors
| Type      | Native connectors | Spark connectors
|-----------|:----------|:----------|
| Databases | [![Big Query](https://ploosh.io/wp-content/uploads/2025/01/bigquery.png)](/docs/docs/connectors-native-big-query/) [![Databricks](https://ploosh.io/wp-content/uploads/2025/01/databricks.png)](/docs/connectors-native-databricks) [![Snowflake](https://ploosh.io/wp-content/uploads/2025/01/snowflake.png)](/docs/connectors-native-snowflake) [![Sql Server](http://ploosh.io/wp-content/uploads/2025/01/mssql.png)](SQL-Server) [![PostgreSQL](https://ploosh.io/wp-content/uploads/2025/01/postgresql.png)](/docs/connectors-native-postgreSQL) [![MySQL](https://ploosh.io/wp-content/uploads/2025/01/mysql.png)](/docs/connectors-native-mysql) | [![SQL](https://ploosh.io/wp-content/uploads/2025/01/sql.png)](/docs/connectors-spark-sql)
| Files     | [![CSV](http://ploosh.io/wp-content/uploads/2025/01/csv.png)](/docs/connectors-native-csv) [![Excel](http://ploosh.io/wp-content/uploads/2025/01/excel.png)](/docs/connectors-native-excel) [![Parquet](http://ploosh.io/wp-content/uploads/2025/01/parquet.png)](/docs/connectors-native-parquet) | [![Delta](http://ploosh.io/wp-content/uploads/2025/01/delta.png)](/docs/connectors-spark-delta) [![CSV](http://ploosh.io/wp-content/uploads/2025/01/csv.png)](/docs/connectors-spark-csv)
| Others    | [![CSV](http://ploosh.io/wp-content/uploads/2025/01/empty.png)](/docs/connectors-native-empty) | [![Empty](http://ploosh.io/wp-content/uploads/2025/01/empty.png)](/docs/connectors-spark-empty)
| Not yet but soon    | ![JSON](http://ploosh.io/wp-content/uploads/2025/01/json.png) ![Oracle](http://ploosh.io/wp-content/uploads/2025/01/oracle.png) | ![Parquet](http://ploosh.io/wp-content/uploads/2025/01/parquet.png)

# Get started

## Steps
1. Install Ploosh package
2. Setup connection file
3. Setup test cases
4. Run tests
4. Get results

## Install Ploosh package
Install from [PyPi](https://pypi.org/project/ploosh/) package manager:
``` shell
pip install ploosh
```

## Setup connection file
Add a yaml file with name "connections.yml" and following content:
``` yaml
mssql_getstarted:
  type: mysql
  hostname: my_server_name.database.windows.net
  database: my_database_name
  username: my_user_name
  // using a parameter is highly recommended
  password: $var.my_sql_server_password 
```

## Setup test cases
Add a folder "test_cases" with a yaml file with any name. In this example "example.yaml". Add the following content:

``` yaml
Test aggregated data:
  options:
    sort:
      - gender
      - domain
  source:
    connection: mysql_demo
    type: mysql
    query: | 
      select gender, right(email, length(email) - position("@" in email)) as domain, count(*) as count
        from users
        group by gender, domain
  expected:
    type: csv
    path: ./data/test_target_agg.csv

Test invalid data:
  source:
    connection: mysql_demo
    type: mysql
    query: | 
      select id, first_name, last_name, email, gender, ip_address
        from users 
        where email like "%%.gov"
  expected:
    type: empty
```

## Run tests
``` shell
ploosh --connections "connections.yml" --cases "test_cases" --export "JSON" --p_my_sql_server_password "mypassword"
```

![Execution result]([images/execution.png](http://ploosh.io/wp-content/uploads/2024/09/image.png))

## Test results

``` json
[
  {
    "name": "Test aggregated data",
    "state": "passed",
    "source": {
      "start": "2024-02-05T17:08:36Z",
      "end": "2024-02-05T17:08:36Z",
      "duration": 0.0032982
    },
    "expected": {
      "start": "2024-02-05T17:08:36Z",
      "end": "2024-02-05T17:08:36Z",
      "duration": 6.0933333333333335e-05
    },
    "compare": {
      "start": "2024-02-05T17:08:36Z",
      "end": "2024-02-05T17:08:36Z",
      "duration": 0.00046468333333333334
    }
  },
  {
    "name": "Test invalid data",
    "state": "failed",
    "source": {
      "start": "2024-02-05T17:08:36Z",
      "end": "2024-02-05T17:08:36Z",
      "duration": 0.00178865
    },
    "expected": {
      "start": "2024-02-05T17:08:36Z",
      "end": "2024-02-05T17:08:36Z",
      "duration": 1.49e-05
    },
    "compare": {
      "start": "2024-02-05T17:08:36Z",
      "end": "2024-02-05T17:08:36Z",
      "duration": 1.8333333333333333e-07
    },
    "error": {
      "type": "count",
      "message": "The count in source dataset (55) is different than the count in the expected dataset (0)"
    }
  }
]
```

# Run with spark
It's possible to run the tests with spark. To do that, you need to install the spark package or use a platform that already has it installed like Databricks or Microsoft Fabric.

See the [Spark connector](/docs/configuration-spark-mode/) for more information.
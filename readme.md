# Ploosh

Ploosh is yaml based framework used to automatized the testing process in data projects. 

# Get started
Go to the [ploosh documentation](https://ploosh.io/docs/ploosh/) to find the get started tutorial.

## Steps
1. Install ploosh package
2. Run tests
3. Analyse results

## Install Ploosh

Install from [PyPi](https://pypi.org/project/ploosh/) package manager:
``` shell
pip install ploosh
```

## Run tests
``` shell
ploosh --connections "connections.yml" --cases "test_cases" --export "JSON" --p_my_sql_server_password "mypassword"
```

![Execution result](http://ploosh.io/wp-content/uploads/2024/09/image.png)

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
    "name": "Test unvalid data",
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
      "message": "The count in source dataset (55) is differant than the count the in expected dataset (0)"
    }
  }
]
```

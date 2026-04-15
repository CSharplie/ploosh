# Add a new connector

This guide explains how to create a new connector for Ploosh. A connector is a Python class that fetches data from a source and returns it as a DataFrame.

## Architecture overview

Ploosh discovers connectors **automatically** at startup. The `__init__.py` file in `src/ploosh/connectors/` scans all files matching the pattern `connector_*.py`, imports them, and registers every class whose name starts with `Connector`.

There is **no registry to update** and **no configuration to change**: simply creating a correctly named file is enough.

```
src/ploosh/connectors/
├── connector.py               # Base class
├── connector_csv.py           # Example: native connector
├── connector_csv_spark.py     # Example: Spark connector
├── connector_<your_name>.py   # ← Your new connector
└── __init__.py                # Auto-discovery logic
```

## Step 1 — Create the connector file

Create a new file in `src/ploosh/connectors/` with the naming convention:

| Type | File name |
|------|-----------|
| Native (Pandas) | `connector_<name>.py` |
| Spark | `connector_<name>_spark.py` |

## Step 2 — Implement the class

Every connector extends the `Connector` base class and must:

1. Set `name` — the identifier used in YAML files (`type: <NAME>`)
2. Set `connection_definition` — parameters declared in `connections.yml`
3. Set `configuration_definition` — parameters declared in test case YAML
4. Implement `get_data()` — returns a `pandas.DataFrame` (native) or a Spark `DataFrame` (Spark)
5. Set `executed_action` — the query, file path or command that was executed (used in logs)

### Base class reference

```python
class Connector:
    name = None
    connection_definition = None
    configuration_definition = None
    is_spark = False
    spark = None
    executed_action = None

    def get_data(self, configuration: dict, connection: dict):
        return None

    def get_executed_action(self):
        return self.executed_action
```

### Minimal native connector

```python
"""Connector to read data from FooBar"""

import pandas as pd
from connectors.connector import Connector


class ConnectorFooBar(Connector):
    """Connector to read data from FooBar"""

    def __init__(self):
        self.name = "FOOBAR"
        self.connection_definition = []
        self.configuration_definition = [
            {"name": "path"},
        ]

    def get_data(self, configuration: dict, connection: dict):
        self.executed_action = configuration["path"]

        df = pd.read_csv(configuration["path"])
        return df
```

### Minimal Spark connector

```python
"""Connector to read data from FooBar with Spark"""

from connectors.connector import Connector


class ConnectorFooBarSpark(Connector):
    """Connector to read data from FooBar with Spark"""

    def __init__(self):
        self.name = "FOOBAR_SPARK"
        self.is_spark = True
        self.connection_definition = []
        self.configuration_definition = [
            {"name": "path"},
        ]

    def get_data(self, configuration: dict, connection: dict):
        self.executed_action = configuration["path"]

        df = self.spark.read.format("foobar").load(configuration["path"])
        return df
```

> For Spark connectors, the Spark session is automatically injected into `self.spark` by the framework at startup.

## Step 3 — Define parameters

Parameters are validated and resolved at runtime by [pyjeb](https://github.com/CSharplie/pyjeb) via the `control_and_setup` function. This library handles default values, type casting, required field validation and `validset` enforcement. You only need to declare the parameter definitions — Ploosh and pyjeb take care of the rest.

Each parameter is a dictionary with the following keys:

| Key | Required | Description |
|-----|----------|-------------|
| `name` | Yes | Parameter name, used as key in YAML |
| `default` | No | Default value. If absent, the parameter is **required** |
| `type` | No | Type cast: `string`, `integer`, `decimal`, `boolean`, `list`, `dict` |
| `validset` | No | List of allowed values |

### connection_definition

These parameters are declared in `connections.yml` and shared across all test cases using this connection.

```python
self.connection_definition = [
    {
        "name": "mode",
        "default": "password",
        "validset": ["password", "connection_string"],
    },
    {"name": "hostname", "default": None},
    {"name": "database", "default": None},
    {"name": "username", "default": None},
    {"name": "password", "default": None},
    {"name": "port", "default": 3306, "type": "integer"},
    {"name": "connection_string", "default": None},
]
```

> Parameters with `"default": None` are optional. Parameters without `default` are required.

### configuration_definition

These parameters are declared in the test case YAML, under `source` or `expected`.

```python
self.configuration_definition = [
    {"name": "query"},                           # Required
    {"name": "connection"},                      # Required
    {"name": "timeout", "type": "integer", "default": 30},  # Optional
]
```

## Step 4 — Implement get_data()

The `get_data` method receives two dictionaries:

| Parameter | Description |
|-----------|-------------|
| `configuration` | Resolved test case parameters (from `configuration_definition`) |
| `connection` | Resolved connection parameters (from `connection_definition`), or `None` if no connection is needed |

The method must:

1. Set `self.executed_action` with a meaningful description (query, file path, etc.)
2. Return a DataFrame — `pandas.DataFrame` for native connectors, Spark `DataFrame` for Spark connectors

Parameter values are already validated and defaults are applied by the framework using `pyjeb.control_and_setup` before `get_data()` is called.

### Example with connection

```python
def get_data(self, configuration: dict, connection: dict):
    hostname = connection["hostname"]
    database = connection["database"]
    query = configuration["query"]

    self.executed_action = query

    engine = create_engine(f"foobar://{hostname}/{database}")
    df = pd.read_sql(query, engine)
    return df
```

## Step 5 — Add dependencies

If your connector requires an external Python package, you need to add it in several places:

### 1. `src/requirements.txt`

Add the package with a pinned version:

```
my-package==1.2.3
```

### 2. `src/setup.py` or `src/setup-full.py`

Ploosh is published as two PyPI packages:

| Package | Setup file | Scope |
|---------|-----------|-------|
| `ploosh-core` | `src/setup-core.py` | Lightweight — no connector-specific dependencies |
| `ploosh` | `src/setup-full.py` | Full — all connector dependencies included |

- If your dependency is a **core library** needed by the framework itself (e.g. pandas, pyjeb), add it to the `install_requires` list in `src/setup.py`.
- If your dependency is **specific to your connector** (e.g. a database driver), add it to the `install_requires` list in `src/setup-full.py`.

```python
# src/setup-full.py
install_requires = [
    # ... existing dependencies
    "my-package==1.2.3",
]
```

> The `ploosh-core` package imports connectors with a `try/except` — if a dependency is missing, the connector is simply skipped with a warning. This allows `ploosh-core` to work without all dependencies installed.

## Step 6 — Add unit tests

Create a test file in `tests/connectors/` named `test_<name>.py`.

The tests should:

1. Instantiate the connector
2. Prepare `configuration` and `connection` dictionaries
3. Call `control_and_setup` to apply defaults (same behavior as the framework)
4. Call `get_data` and validate the result

```python
import pandas as pd
import pytest
from pyjeb import control_and_setup
from ploosh.connectors.connector_foobar import ConnectorFooBar


@pytest.fixture
def connector():
    return ConnectorFooBar()


def test_get_data(connector):
    configuration = {"path": "./tests/.data/sample.csv"}
    connection = {}

    configuration = control_and_setup(configuration, connector.configuration_definition)
    connection = control_and_setup(connection, connector.connection_definition)

    df = connector.get_data(configuration, connection)

    assert not df.empty
    assert connector.executed_action == "./tests/.data/sample.csv"
```

Run the tests with:

```shell
pytest tests/connectors/test_foobar.py -v
```

## Step 7 — Add documentation

Create a documentation page in `docs/connectors/native/` or `docs/connectors/spark/` following the existing format. Each connector page should include:

- A short description
- The list of connection parameters (if any) with types and defaults
- The list of configuration parameters with types and defaults
- A complete YAML example showing `connections.yml` and a test case

## YAML usage after creation

Once the file is created, users can immediately use the connector in their test cases:

```yaml
# connections.yml (only if connection_definition is not empty)
my_foobar:
  type: foobar
  hostname: localhost
  database: mydb
```

```yaml
# test_case.yml
Test FooBar data:
  source:
    type: foobar
    connection: my_foobar
    query: "SELECT * FROM my_table"
  expected:
    type: csv
    path: ./expected/my_table.csv
```

> The `type` value in YAML is case-insensitive and maps to the `name` attribute of the connector class.

## Checklist

- [ ] File created as `connector_<name>.py` in `src/ploosh/connectors/`
- [ ] Class extends `Connector` and name starts with `Connector`
- [ ] `name` is set (uppercase, unique)
- [ ] `connection_definition` is set (empty list `[]` if no connection needed)
- [ ] `configuration_definition` is set
- [ ] `is_spark = True` if it's a Spark connector
- [ ] `get_data()` returns a DataFrame
- [ ] `executed_action` is set in `get_data()`
- [ ] Unit tests added in `tests/connectors/`
- [ ] Documentation added in `docs/connectors/`

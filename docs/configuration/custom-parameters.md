# Custom parameters

Custom parameters allow you to avoid hardcoding sensitive information like passwords or environment-specific values in your YAML configuration files.

## Syntax

Use the `$var.<parameter_name>` syntax in your YAML files to reference a custom parameter.

## Passing values

### Command line

Pass the parameter value using `--p_<parameter_name>`:

``` shell
ploosh --connections connections.yml --cases test_cases --p_db_password "my_secret" --p_environment "production"
```

### Python API

Pass variables as a dictionary:

``` python
from ploosh import execute_cases

execute_cases(
    cases="test_cases",
    connections="connections.yml",
    variables={
        "db_password": "my_secret",
        "environment": "production"
    }
)
```

## Usage in connections

``` yaml
connections:
  my_database:
    type: mysql
    hostname: my-server.database.windows.net
    database: my_database
    username: my_user
    password: $var.db_password
```

## Usage in test cases

``` yaml
Test with parameter:
  source:
    type: mysql
    connection: my_database
    query: |
      SELECT *
      FROM $var.environment.employees
  expected:
    type: empty
```

## CI/CD usage

In CI/CD pipelines, pass parameters from secure variable groups or secrets:

### Azure DevOps

``` yaml
- task: CmdLine@2
  inputs:
    script: ploosh --connections connections.yml --cases test_cases --p_db_password "$(db_password)"
```

### GitHub Actions

``` yaml
- run: ploosh --connections connections.yml --cases test_cases --p_db_password "${{ secrets.DB_PASSWORD }}"
```

## Security

- Never commit sensitive values (passwords, tokens) in YAML files
- Always use `$var` references and pass values at runtime
- In CI/CD, store secrets in variable groups or secret stores

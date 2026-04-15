# GitHub Actions

Ploosh can be integrated into GitHub Actions workflows for automated data testing.

## Example workflow

``` yaml
name: Data Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install ODBC Driver (if using SQL Server)
        run: |
          curl https://packages.microsoft.com/keys/microsoft.asc | sudo tee /etc/apt/trusted.gpg.d/microsoft.asc
          curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list
          sudo apt-get update
          sudo ACCEPT_EULA=Y apt-get install -y msodbcsql18

      - name: Install Ploosh
        run: pip install ploosh

      - name: Run tests
        run: |
          ploosh \
            --connections "connections.yml" \
            --cases "test_cases" \
            --export "JSON" \
            --failure false \
            --p_db_password "${{ secrets.DB_PASSWORD }}"

      - name: Upload test results
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: test-results
          path: output/
```

## Using TRX format

If you want to integrate with test result viewers:

``` yaml
      - name: Run tests (TRX)
        run: |
          ploosh \
            --connections "connections.yml" \
            --cases "test_cases" \
            --export "TRX" \
            --failure false \
            --p_db_password "${{ secrets.DB_PASSWORD }}"

      - name: Upload TRX results
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: trx-results
          path: output/trx/
```

## Secrets management

Store sensitive values in GitHub repository secrets:

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Add secrets (e.g. `DB_PASSWORD`, `SNOWFLAKE_PASSWORD`)
3. Reference them in the workflow as `${{ secrets.SECRET_NAME }}`

## Tips

- Set `--failure false` to ensure the workflow completes and uploads results even when tests fail
- Use the `if: always()` condition on the upload step to capture results regardless of test outcomes
- Store connection files in the repository (with `$var` references for secrets)

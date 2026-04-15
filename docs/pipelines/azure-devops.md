Ploosh is easy to use and can be integrated with any CI/CD pipeline. 
The following steps are required to run Ploosh tests in Azure DevOps and publish the results into Azure DevOps Test Plans.

# Exemple of pipeline

1. Install ODBC driver for SQL Server if SQL Server connector is used
2. Install Ploosh package from PyPi
3. Execute Ploosh
    1. Provide the connections file
    2. Provide the test cases folder
    3. Provide the export format (TRX for Azure DevOps Test Plans)
    4. Disable the failure flag to avoid the pipeline to fail if a test fails
    5. Provide the passwords as parameters from the variables group
4. Publish test results

```yaml
trigger:
- main

variables:
- group: demo
stages:
  - stage: 
    displayName: Build
    jobs:
      - job: 
        steps:
          - checkout: self
          - task: CmdLine@2
            displayName: Install ODBC driver for SQL Server
            inputs:
              script: |
                curl https://packages.microsoft.com/keys/microsoft.asc | sudo tee /etc/apt/trusted.gpg.d/microsoft.asc
                curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list
                sudo apt-get update
                sudo ACCEPT_EULA=Y apt-get install -y msodbcsql18
          - task: CmdLine@2
            displayName: Install ploosh
            inputs:
              script: |
                pip install ploosh
          - task: CmdLine@2
            displayName: Execute ploosh
            inputs:
              script: ploosh  --connections "connections.yml" --cases "test_cases" --export "TRX" --failure False --p_mysql_password_db "$(mysql_password)" --p_mssql_password_db "$(mssql_password)" --p_postgresql_password_db "$(postgresql_password)"
          - task: PublishTestResults@2
            inputs:
              testResultsFormat: 'VSTest'
              testResultsFiles: '*.xml'
              searchFolder: 'output/trx/'
              mergeTestResults: true
              testRunTitle: '$(Build.DefinitionName)'
```
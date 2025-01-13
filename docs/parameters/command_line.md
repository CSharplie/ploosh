# Mandatory arguments
- `--connection <connection_file>`: The connection file name to use
- `--cases <case_folder>`: The test case folder where the test cases yaml files are stored

# Optional arguments
- `--export <export_type>`: The export format to use. Can be `JSON`, `CSV` or `TRX`. Default is `JSON`
- `--filter <wildcard>`: A wildcard to filter the test cases to execute. The default value is `*.yml` which means all the test cases will be executed
- `--p_<parameter_name> <parameter_value>`: The parameter value to use. The parameter name is the name of the parameter in the connection file. The parameter value can be passed as an environment variable or as a command line argument
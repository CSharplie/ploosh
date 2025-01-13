# Custom parameters usefulness
It is possible to add a custom parameter in the connection configuration file to avoid hardcoding sensitive information like passwords or credentials.

To use a custom parameter, you need to add a parameter in the connection configuration file and use it in the connection configuration. The parameter value can be passed as an environment variable or as a command line argument.

# Syntax and usage
The syntax of for the parameter is `$var.<parameter_name>` in the connection configuration file.

The parameter value can be passed as a command line argument using the `--p_<parameter_name>` option.
import pathlib
import re
import yaml
from pyjeb import control_and_setup
from core.connectors import get_connection_configuration

def get_connections(root_directory, argv):
    with open(f"{root_directory}/connections.yml") as f:
        content = f.read()
        connections = yaml.safe_load(content)

    # get variables from args and convert to dict
    variables = {}
    for arg in argv:
        result = re.search(r"v_([\w]+)=(.*)", arg)
        if result is not None:
            name = result.group(1)
            value = result.group(2)
            variables[name] = value

    # apply control on each configuration
    for connection_name in connections:
        connection_type = connections[connection_name]["type"]
        connection_configuration = get_connection_configuration(connection_type)
        connections[connection_name] = control_and_setup(connections[connection_name], connection_configuration, variables=variables, functions=None)

    return connections

def get_settings(root_directory):
    with open(f"{root_directory}/settings.yml") as f:
        connections = yaml.load(f, Loader = yaml.loader.SafeLoader)
    return connections


def get_test_cases(root_directory):
    files_list = list(pathlib.Path(f"{root_directory}/test_cases").rglob("*.yml"))

    test_cases = None
    for file_path in files_list:
        with open(file_path) as f:
            configuration = yaml.load(f, Loader = yaml.loader.SafeLoader)
            if(test_cases is None):
                test_cases = configuration
            else:
                for key in configuration.keys():
                    test_cases[key] = configuration[key]

    return test_cases

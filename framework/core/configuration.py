import pathlib
import re
import yaml

def get_connections(root_directory, argv):
    with open(f"{root_directory}/connections.yml") as f:
        content = f.read()
        for arg in argv:
            result = re.search(r"v_([\w]+)=(.*)", arg)
            if result is not None:
                name = result.group(1)
                value = result.group(2)
                content = content.replace(f"{{{name}}}", value)
        connections = yaml.safe_load(content)
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
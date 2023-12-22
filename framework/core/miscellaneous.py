import logging
from core.setup import DEBUG_LEVEL_PRINT
from sys import path

def print_log(message, level = DEBUG_LEVEL_PRINT):
    l = logging.getLogger()
    l.setLevel(level)
    l.log(level, message)

def get_parameter_value(configuration, name, error_code, default = None):
    if name not in configuration.keys() and default is None:
        raise f"{error_code} - The parameter '{name}' must be provided"
    elif name not in configuration.keys() and default is not None:
        return default

    return configuration[name]

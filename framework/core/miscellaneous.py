import logging
import os
from sys import path

run_path = os.path.dirname(__file__)
root_directory = os.path.abspath(f"{run_path}/../")
path.append(f"{root_directory}/framework/resources")

DEBUG_LEVEL_PRINT = 25
logging.addLevelName(25, "INFO")
def logging_print(self, message, *args, **kws):
    self._log(DEBUG_LEVEL_PRINT, message, args, **kws)

logging.Logger.print = logging_print
logging.basicConfig(format = "[%(asctime)s] [%(levelname)s] [%(message)s]", datefmt = "%Y-%m-%d %H:%M:%S", level = 25)

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

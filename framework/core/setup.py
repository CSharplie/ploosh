import logging
import os
from sys import path

run_path = os.path.dirname(__file__)
ROOT_DIRECTORY = os.path.abspath(f"{run_path}/../../")
path.append(f"{ROOT_DIRECTORY}/framework/resources")

DEBUG_LEVEL_PRINT = 25
logging.addLevelName(25, "INFO")
def logging_print(self, message, *args, **kws):
    self._log(DEBUG_LEVEL_PRINT, message, args, **kws)

logging.Logger.print = logging_print
logging.basicConfig(format = "[%(asctime)s] [%(levelname)s] [%(message)s]", datefmt = "%Y-%m-%d %H:%M:%S", level = 25)
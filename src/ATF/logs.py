"""Module for log functions"""
import logging

INFO_LEVEL_PRINT = 25
ERROR_LEVEL_PRINT = 40

LOG_FORMAT_DATE = "%Y-%m-%d %H:%M:%S"
LOG_FORMAT_STRING = "[%(asctime)s] [%(levelname)s] [%(message)s]"

logging.addLevelName(INFO_LEVEL_PRINT, "INFO")
def logging_print(self, message, *args, **kws):
    """Print with info level"""
    self._log(INFO_LEVEL_PRINT, message, args, **kws)

logging.Logger.print = logging_print
logging.basicConfig(format = LOG_FORMAT_STRING, datefmt = LOG_FORMAT_DATE, level = INFO_LEVEL_PRINT)

class Log:
    """Log class contain all functions to log"""
    @staticmethod
    def print(message:str, level:int = INFO_LEVEL_PRINT):
        """Print a message with all metadata informations"""
        log = logging.getLogger()
        log.setLevel(level)
        log.log(level, message)

    @staticmethod
    def print_error(message:str):
        """Print an error message with all metadata informations"""
        Log.print(message, ERROR_LEVEL_PRINT)

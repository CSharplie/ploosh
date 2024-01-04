"""Module for log functions"""
from datetime import datetime
from colorama import Fore, Style

LEVELS_PRINT = {
    "INFO": Fore.GREEN,
    "WARN": Fore.YELLOW,
    "ERROR": Fore.RED
}

LOG_FORMAT_DATE = "%Y-%m-%d %H:%M:%S"
LOG_FORMAT_STRING = f"{Fore.CYAN}[%(asctime)s]{Style.RESET_ALL} <LEVEL_COLOR>[%(levelname)s]{Style.RESET_ALL}[%(message)s]"


class Log:
    """Log class contain all functions to log"""
    @staticmethod
    def print(message:str, level:str = "INFO"):
        """Print a message with all metadata informations"""

        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(f"{Fore.CYAN}[{date_time}] {LEVELS_PRINT[level]}[{level}]{Style.RESET_ALL} {message}")

    @staticmethod
    def print_error(message:str):
        """Print an error message with all metadata informations"""
        Log.print(message, "ERROR")

    @staticmethod
    def print_warning(message:str):
        """Print an warning message with all metadata informations"""
        Log.print(message, "WARN")
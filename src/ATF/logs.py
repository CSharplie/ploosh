"""Module for log functions"""
from datetime import datetime
import os
import re
from colorama import Fore, Style, Back

LEVELS_PRINT = {
    "INFO": Fore.GREEN,
    "WARN": Fore.YELLOW,
    "ERROR": Fore.RED
}


CONSOLE_WIDTH = os.get_terminal_size().columns
CONSOLE_WIDTH_GAP = 29

LOG_FORMAT_DATE = "%Y-%m-%d %H:%M:%S"
LOG_FORMAT_STRING = f"{Fore.CYAN}[%(asctime)s]{Style.RESET_ALL} <LEVEL_COLOR>[%(levelname)s]{Style.RESET_ALL}[%(message)s]"


class Log:
    """Log class contain all functions to log"""
    @staticmethod
    def print(message:str, level:str = "INFO"):
        """Print a message with all metadata informations"""

        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if "[...]" in message:
            without_color = re.sub(r'[^\w ]*[\d]+m', '', message)
            feed_characters = "." * (CONSOLE_WIDTH - CONSOLE_WIDTH_GAP - len(without_color) + 5)
            message = message.replace("[...]", feed_characters)

        print(f"{Fore.CYAN}[{date_time}] {LEVELS_PRINT[level]}[{level}]{Style.RESET_ALL} {message}{Style.RESET_ALL}")

    @staticmethod
    def print_error(message:str):
        """Print an error message with all metadata informations"""
        Log.print(message, "ERROR")

    @staticmethod
    def print_warning(message:str):
        """Print an warning message with all metadata informations"""
        Log.print(message, "WARN")
"""Module for log functions"""
from datetime import datetime
import re
import math
import shutil
from colorama import Fore, Style

LEVELS_PRINT = {
    "INFO": Fore.GREEN,
    "WARN": Fore.YELLOW,
    "ERRO": Fore.RED
}

CONSOLE_WIDTH = shutil.get_terminal_size(fallback=(120, 50)).columns
CONSOLE_WIDTH_GAP = 29
CONSOLE_LOG_SPACE = CONSOLE_WIDTH - CONSOLE_WIDTH_GAP

LOG_FORMAT_DATE = "%Y-%m-%d %H:%M:%S"
LOG_FORMAT_STRING = f"{Fore.CYAN}[%(asctime)s]{Style.RESET_ALL} <LEVEL_COLOR>[%(levelname)s]{Style.RESET_ALL}[%(message)s]"


class Log:
    """Log class contain all functions to log"""
    @staticmethod
    def print(message:str, level:str = "INFO", filler:str = "."):
        """Print a message with all metadata informations"""

        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        count_filler = 1 if message.count("[...]") == 0 else message.count("[...]")
        
        raw_message = re.sub(r'[^\w ]*[\d]+m', '', message)
        print_length = len(raw_message)
        feed_characters = filler * math.trunc((CONSOLE_LOG_SPACE - print_length + (5 * count_filler)) / count_filler)
        message = message.replace("[...]", feed_characters)

        rows_to_print = [message]
        # coloration will be disabled for multi ligne message
        if print_length > CONSOLE_LOG_SPACE or "\n" in message:
            rows_to_print = []
            message_rows = raw_message.split("\n")
            for row in message_rows:
                rows_count = math.ceil(len(row) / CONSOLE_LOG_SPACE)
                for i in range(0, rows_count):
                    start = i * CONSOLE_LOG_SPACE
                    end = (i + 1) * CONSOLE_LOG_SPACE
                    rows_to_print.append(row[start:end])

        for row in rows_to_print:
            print(f"{Fore.CYAN}[{date_time}] {LEVELS_PRINT[level]}[{level}]{Style.RESET_ALL} {row}{Style.RESET_ALL}")

    @staticmethod
    def print_error(message:str):
        """Print an error message with all metadata informations"""
        Log.print(message, "ERRO")

    @staticmethod
    def print_warning(message:str):
        """Print an warning message with all metadata informations"""
        Log.print(message, "WARN")

    @staticmethod
    def print_logo():
        """Print the ATF logo"""

        Log.print("[...]", filler="#")
        Log.print("#[...]       .__                      .__     [...]#", filler=" ")
        Log.print("#[...]______ |  |   ____   ____  _____|  |__  [...]#", filler=" ")
        Log.print("#[...]\____ \|  |  /  _ \ /  _ \/  ___|  |  \ [...]#", filler=" ")
        Log.print("#[...]|  |_> |  |_(  <_> (  <_> \___ \|   Y  \[...]#", filler=" ")
        Log.print("#[...]|   __/|____/\____/ \____/____  |___|  /[...]#", filler=" ")
        Log.print("#[...]|__|                          \/     \/ [...]#", filler=" ")
        Log.print("#[...]Automatized Testing Framework [...]#", filler=" ")
        Log.print("#[...]#", filler=" ")
        Log.print("#[...]https://github.com/CSharplie/Ploosh #", filler=" ")
        Log.print("[...]", filler="#")

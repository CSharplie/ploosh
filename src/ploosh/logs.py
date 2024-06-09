"""Module for log functions"""

import os
import re
import math
import shutil
from datetime import datetime
from colorama import Fore, Style
from version import PLOOSH_VERSION


class Log:
    """Log class contain all functions to log"""

    @staticmethod
    def init():
        Log.LEVELS_PRINT = {
            "INFO": Fore.GREEN,
            "WARN": Fore.YELLOW,
            "ERRO": Fore.RED
        }

        Log.CONSOLE_WIDTH = shutil.get_terminal_size(fallback=(120, 50)).columns
        Log.CONSOLE_WIDTH_GAP = 29
        Log.CONSOLE_LOG_SPACE = Log.CONSOLE_WIDTH - Log.CONSOLE_WIDTH_GAP

        Log.LOGS_FOLDER = "./logs"
        Log.LOGS_PATH = f"{Log.LOGS_FOLDER}/ploosh_{datetime.now().strftime('%Y%m%d%H%M%S')}.log"

        os.makedirs(Log.LOGS_FOLDER, exist_ok=True)

    @staticmethod
    def print(message:str, level:str = "INFO", filler:str = "."):
        """Print a message with all metadata informations"""

        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        count_filler = 1 if message.count("[...]") == 0 else message.count("[...]")
        
        raw_message = re.sub(r'[^\w ]*[\d]+m', '', message)
        print_length = len(raw_message)
        feed_characters = filler * math.trunc((Log.CONSOLE_LOG_SPACE - print_length + (5 * count_filler)) / count_filler)
        message = message.replace("[...]", feed_characters)

        rows_to_print = [message]
        # coloration will be disabled for multi ligne message
        if print_length > Log.CONSOLE_LOG_SPACE or "\n" in message:
            rows_to_print = []
            message_rows = raw_message.split("\n")
            for row in message_rows:
                rows_count = math.ceil(len(row) / Log.CONSOLE_LOG_SPACE)
                for i in range(0, rows_count):
                    start = i * Log.CONSOLE_LOG_SPACE
                    end = (i + 1) * Log.CONSOLE_LOG_SPACE
                    rows_to_print.append(row[start:end])

        rows_to_print = [f"{Fore.CYAN}[{date_time}] {Log.LEVELS_PRINT[level]}[{level}]{Style.RESET_ALL} {row}{Style.RESET_ALL}" for row in rows_to_print]

        for row in rows_to_print:
            print(row)

        

        with open(Log.LOGS_PATH, "a", encoding="UTF-8") as f:
            log_text = "\r\n".join(rows_to_print) + "\r\n"

            for key in Fore.__dict__:
                log_text = log_text.replace(Fore.__dict__[key], "")

            for key in Style.__dict__:
                log_text = log_text.replace(Style.__dict__[key], "")

            f.write(log_text)

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

        Log.print(f"[...]", filler="~")
        Log.print(f"[...]       .__                      .__     [...]", filler=" ")
        Log.print(f"[...]______ |  |   ____   ____  _____|  |__  [...]", filler=" ")
        Log.print(f"[...]\____ \|  |  /  _ \ /  _ \/  ___|  |  \ [...]", filler=" ")
        Log.print(f"[...]|  |_> |  |_(  <_> (  <_> \___ \|   Y  \[...]", filler=" ")
        Log.print(f"[...]|   __/|____/\____/ \____/____  |___|  /[...]", filler=" ")
        Log.print(f"[...]|__|                          \/     \/ [...]", filler=" ")
        Log.print(f"[...]Automatized Testing Framework (v {PLOOSH_VERSION})[...]", filler=" ")
        Log.print(f"[...]", filler=" ")
        Log.print(f"[...]https://github.com/CSharplie/ploosh", filler=" ")
        Log.print(f"[...]", filler="~")

def print_compare_state(current_case):
    state = current_case.state.upper()
    state_matrix = {
        "FAILED" : { "color": Fore.YELLOW, "function": Log.print_warning },
        "ERROR" : { "color": Fore.RED, "function": Log.print_error },
        "PASSED" : { "color": Fore.GREEN, "function": Log.print },
    }
    state_item = state_matrix[state]
    state_item["function"](f"Compare state: {state_item['color']}{state}")
    
    if state != "PASSED":
        state_item["function"](f"Error type   : {state_item['color']}{current_case.error_type.upper()}")
        state_item["function"](f"Error message: {state_item['color']}{current_case.error_message}")

def print_summary(cases, statistics):
    for case_name in cases:
        state = cases[case_name].state
        color = Fore.CYAN

        if state == "error": color = Fore.RED
        if state == "passed": color = Fore.GREEN
        if state == "failed": color = Fore.YELLOW

        if state == "notExecuted": state = "skipped"

        Log.print(f"{case_name} [...] {color}{state.upper()}")

    message = f"passed: {Fore.GREEN}{statistics.passed}{Style.RESET_ALL}, "
    message += f"failed: {Fore.YELLOW}{statistics.failed}{Style.RESET_ALL}, "
    message += f"error: {Fore.RED}{statistics.error}{Style.RESET_ALL}, "
    message += f"skipped: {Fore.CYAN}{statistics.not_executed}{Style.RESET_ALL}"

    Log.print(message)
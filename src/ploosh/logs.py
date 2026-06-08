"""Module for log functions"""

import math
import os
import re
import shutil
import threading
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.align import Align
from rich.text import Text
from version import PLOOSH_VERSION

class Log:
    """Log class contain all functions to log"""

    FILE_LOCK = threading.Lock()

    @staticmethod
    def init():
        """Initialize log settings and create log directory"""
        Log.LEVELS_PRINT = {
            "INFO": "green",
            "WARN": "yellow",
            "ERRO": "red",
        }

        Log.STATE_PRINT = {
            "progress": "cyan",
            "passed": "green",
            "failed": "yellow",
            "error": "red",
            "notExecuted": "cyan",
            "skipped": "cyan",
        }

        # Get terminal size and set console log space
        Log.CONSOLE_WIDTH = shutil.get_terminal_size(fallback=(120, 50)).columns

        # Set log folder and log file path
        Log.LOGS_FOLDER = "./logs"
        Log.LOGS_PATH = f"{Log.LOGS_FOLDER}/ploosh_{datetime.now().strftime('%Y%m%d%H%M%S')}.log"

        # Create log folder if it doesn't exist
        os.makedirs(Log.LOGS_FOLDER, exist_ok=True)

        # Initialize the console for rich logging 
        Log.console = Console(       
            force_terminal=True, 
            force_jupyter=False,
            width=Log.CONSOLE_WIDTH,
        )

    @staticmethod
    def write_log_line(date_time: str, level: str, message: str):
        """Append one plain-text log line to the log file."""
        with Log.FILE_LOCK:
            with open(Log.LOGS_PATH, "a", encoding="UTF-8") as log_file:
                log_file.write(f"[{date_time}] [{level}] {message}\n")


    def print_message(message: str, level: str = "INFO", no_overflow: bool = False, style: str = None):
        """Print an info message with all metadata informations"""
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        table = Table(box=None, show_header=False, expand=True, padding=(0, 1), pad_edge=False)
        table.add_column("date_time", style="dim", no_wrap=True)
        table.add_column("level", no_wrap=True)
        table.add_column("message", ratio=1, overflow="crop" if no_overflow else "fold")

        level_cell = Text(f"[{level}]", style=Log.LEVELS_PRINT.get(level, "white"))
        message_cell = Text(str(message), style=style) if style else f"{message}"

        table.add_row(f"[{date_time}]", level_cell, message_cell)

        Log.console.print(table)
        Log.write_log_line(date_time, level, str(message))

    def print_case_progress(message: str, level: str = "INFO", state: str = "progress"):
        """Print a progress message with all metadata informations"""
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        table = Table(box=None, show_header=False, expand=True, padding=(0, 1), pad_edge=False)
        table.add_column("date_time", style="dim", no_wrap=True)
        table.add_column("level", no_wrap=True)
        table.add_column("message", ratio=1)
        table.add_column("state", justify="right", no_wrap=True)

        level_cell = Text(f"[{level}]", style=Log.LEVELS_PRINT.get(level, "white"))
        state_cell = Text(state, style=Log.STATE_PRINT.get(state, "white"))
        table.add_row(f"[{date_time}]", level_cell, f"{message}", state_cell)

        Log.console.print(table)
        Log.write_log_line(date_time, level, f"{message} [{state}]")

    @staticmethod
    def print_error(message: str):
        """Print an error message with all metadata informations"""
        Log.print_message(message, "ERRO")

    @staticmethod
    def print_warning(message: str):
        """Print a warning message with all metadata informations"""
        Log.print_message(message, "WARN")

    @staticmethod
    def print_logo():
        """Print the ATF logo"""

        ploosh_logo = "\n"
        ploosh_logo += "           ░██                                  ░██        \n"
        ploosh_logo += "           ░██                                  ░██        \n"
        ploosh_logo += "░████████  ░██  ░███████   ░███████   ░███████  ░████████  \n"
        ploosh_logo += "░██    ░██ ░██ ░██    ░██ ░██    ░██ ░██        ░██    ░██ \n"
        ploosh_logo += "░██    ░██ ░██ ░██    ░██ ░██    ░██  ░███████  ░██    ░██ \n"
        ploosh_logo += "░███   ░██ ░██ ░██    ░██ ░██    ░██        ░██ ░██    ░██ \n"
        ploosh_logo += "░██░█████  ░██  ░███████   ░███████   ░███████  ░██    ░██ \n"
        ploosh_logo += "░██                                                        \n"
        ploosh_logo += "░██                                                        \n"

        ploosh_subtitle = f"Automatized Testing Framework (v{PLOOSH_VERSION})\n"
        ploosh_github_url = "https://github.com/CSharplie/ploosh"

        Log.console.print(Align.center(Text(ploosh_logo, justify="left", no_wrap=True)))
        Log.console.print(Align.center(Text(ploosh_subtitle, style="bold", no_wrap=True)))
        Log.console.print(Align.right(Text(ploosh_github_url, no_wrap=True)))

def print_compare_state(case_name, current_case):
    """Print the comparison state of a test case"""

    if current_case.state == "passed":
        return
    
    message = f"{case_name}\nCompare state: {current_case.state.upper()}\n"
    message += f"Error type   : {current_case.error_type.upper()}\n"
    message += f"Error message: {current_case.error_message}"

    Log.print_warning(message)


def print_summary(cases, statistics):
    """Print a summary of test case results"""
    for case_name in cases:
        state = cases[case_name].state

        if state == "notExecuted":
            state = "skipped"

        Log.print_case_progress(case_name, state=state)

    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    table = Table(box=None, show_header=False, expand=True, padding=(0, 1), pad_edge=False)
    table.add_column("date_time", style="dim", no_wrap=True)
    table.add_column("level", no_wrap=True)
    table.add_column("message", ratio=1)

    level_cell = Text("[INFO]", style=Log.LEVELS_PRINT.get("INFO", "white"))
    summary_cell = Text()
    summary_cell.append("passed: ")
    summary_cell.append(str(statistics.passed), style="green")
    summary_cell.append(", failed: ")
    summary_cell.append(str(statistics.failed), style="yellow")
    summary_cell.append(", error: ")
    summary_cell.append(str(statistics.error), style="red")
    summary_cell.append(", skipped: ")
    summary_cell.append(str(statistics.not_executed), style="cyan")

    table.add_row(f"[{date_time}]", level_cell, summary_cell)
    Log.console.print(table)
    Log.write_log_line(
        date_time,
        "INFO",
        (
            f"passed: {statistics.passed}, failed: {statistics.failed}, "
            f"error: {statistics.error}, skipped: {statistics.not_executed}"
        ),
    )

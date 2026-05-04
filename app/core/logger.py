"""Logger module for Save Restricted Content Bot.

This module provides a simple file and console logging system with different
log levels (INFO, WARNING, ERROR). All logs are timestamped and prefixed with
the module name for easy debugging.

Typical usage:
    from app.core.logger import log
    log.info("Operation started", "ModuleName")
    log.warning("Unusual behavior detected", "ModuleName")
    log.error("An error occurred", "ModuleName")
"""

import os
from datetime import datetime


class Logger:
    """A simple file and console logger with multiple log levels.

    This logger writes to both the console and a log file in the data/logs
    directory. Each log entry is timestamped and includes the module name.

    Attributes:
        logFileName (str): Name of the log file.
        logFilePath (str): Full path to the log file.
    """

    def __init__(self, logFileName: str) -> None:
        """Initialize the logger.

        Args:
            logFileName (str): Name of the log file to create.
        """
        self.logFileName = logFileName
        self.logFilePath = ""

        if self.logFileName:
            self.create_log_file()

    def create_log_file(self) -> None:
        """Create the log file and its parent directories.

        Creates the data/logs directory structure if it doesn't exist
        and initializes the log file with a header.
        """
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        log_dir = os.path.join(base_dir, "data", "logs")
        self.logFilePath = os.path.join(log_dir, self.logFileName)

        os.makedirs(log_dir, exist_ok=True)

        if not os.path.exists(self.logFilePath):
            with open(self.logFilePath, "w", encoding="utf-8") as f:
                f.write("=" * 60 + "\n")
                f.write("SAVE-RESTRICTED-CONTENT-BOT-LOGS\n")
                f.write("=" * 60 + "\n\n")

    def _write(self, level: str, msg: str, module: str = "Core") -> None:
        """Write a log message to console and file.

        Args:
            level (str): Log level (INFO, WARNING, ERROR).
            msg (str): The log message.
            module (str): Module name where the log originated. Defaults to "Core".
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log = f"[{timestamp}] [{level}] [{module}] {msg}"

        print(log)

        if self.logFilePath:
            with open(self.logFilePath, "a", encoding="utf-8") as f:
                f.write(log + "\n")

    def info(self, msg: str, module: str = "Core") -> None:
        """Log an info message.

        Args:
            msg (str): The info message.
            module (str): Module name. Defaults to "Core".
        """
        self._write("INFO", msg, module)

    def warning(self, msg: str, module: str = "Core") -> None:
        """Log a warning message.

        Args:
            msg (str): The warning message.
            module (str): Module name. Defaults to "Core".
        """
        self._write("WARNING", msg, module)

    def error(self, msg: str, module: str = "Core") -> None:
        """Log an error message.

        Args:
            msg (str): The error message.
            module (str): Module name. Defaults to "Core".
        """
        self._write("ERROR", msg, module)


logFileName = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
log = Logger(logFileName)

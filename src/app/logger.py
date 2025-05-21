# -----------------------------------------------------------------------------
# Skryper - A tool to scan, analyze, and organize your project file structures
#
# Copyright (c) 2024 Jonas Zeihe
# Licensed under the MIT License. See LICENSE file in the project root for details.
#
# Project URL: https://github.com/jonaszeihe/skryper
# Contact: JonasZeihe@gmail.com
# -----------------------------------------------------------------------------

"""
Logger component for the directory scanning application.

This module provides functions to set up a logger that captures logs in memory
and later saves them to a file.
"""

# logger.py

import logging
from pathlib import Path
from io import StringIO


def setup_logger(log_level=logging.INFO) -> (logging.Logger, StringIO):
    """
    Sets up the logger for the application.

    Logs are simultaneously written to memory (for optional saving to file)
    and to the console.

    Args:
        log_level (int): Logging level (default: logging.INFO)

    Returns:
        Tuple[Logger, StringIO]: Configured logger and in-memory log stream.
    """
    logger = logging.getLogger("DirectoryScanner")
    logger.setLevel(log_level)

    log_stream = StringIO()

    stream_handler = create_stream_handler(log_stream, log_level)
    logger.addHandler(stream_handler)

    console_handler = create_console_handler(log_level)
    logger.addHandler(console_handler)

    return logger, log_stream


def create_stream_handler(
    log_stream: StringIO, log_level: int
) -> logging.StreamHandler:
    """
    Creates a stream handler for in-memory logging.

    Args:
        log_stream (StringIO): The stream where logs will be stored.
        log_level (int): Logging level for this handler.

    Returns:
        logging.StreamHandler: Configured in-memory log handler.
    """
    handler = logging.StreamHandler(log_stream)
    handler.setLevel(log_level)
    handler.setFormatter(create_log_formatter())
    return handler


def create_console_handler(log_level: int) -> logging.StreamHandler:
    """
    Creates a console handler for logging to stdout.

    Args:
        log_level (int): Logging level for this handler.

    Returns:
        logging.StreamHandler: Configured console handler.
    """
    handler = logging.StreamHandler()
    handler.setLevel(log_level)
    handler.setFormatter(create_log_formatter())
    return handler


def create_log_formatter() -> logging.Formatter:
    """
    Creates a standard formatter for all log handlers.

    Returns:
        logging.Formatter: Formatter instance with timestamp and log level.
    """
    return logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")


def save_logs_to_file(log_stream: StringIO, log_path: Path) -> None:
    """
    Saves the in-memory logs to a specified log file.

    Args:
        log_stream (StringIO): The in-memory log stream.
        log_path (Path): Full path where the log file will be saved.
    """
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("w", encoding="utf-8") as file:
        file.write(log_stream.getvalue())

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
from datetime import datetime
from pathlib import Path
from io import StringIO


def setup_logger(log_level=logging.INFO) -> (logging.Logger, StringIO):
    """
    Sets up the logger for the application. Logs are stored in memory and can be written to a file later.

    Args:
        log_level (int, optional): The logging level (e.g., logging.INFO, logging.DEBUG). Defaults to logging.INFO.

    Returns:
        logging.Logger: Configured logger instance.
        StringIO: Log stream to store logs in memory.
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
        log_level (int): The logging level for the handler.

    Returns:
        logging.StreamHandler: Configured stream handler.
    """
    stream_handler = logging.StreamHandler(log_stream)
    stream_handler.setLevel(log_level)
    stream_handler.setFormatter(create_log_formatter())
    return stream_handler


def create_console_handler(log_level: int) -> logging.StreamHandler:
    """
    Creates a console handler for logging to stdout.

    Args:
        log_level (int): The logging level for the handler.

    Returns:
        logging.StreamHandler: Configured console handler.
    """
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(create_log_formatter())
    return console_handler


def create_log_formatter() -> logging.Formatter:
    """
    Creates a standard log formatter for all log handlers.

    Returns:
        logging.Formatter: The log formatter.
    """
    return logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")


def save_logs_to_file(log_stream: StringIO, log_dir: Path = Path(".")) -> None:
    """
    Saves the in-memory logs to a log file.

    Args:
        log_stream (StringIO): The in-memory log stream.
        log_dir (Path): The directory where the log file will be saved.
    """
    log_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"{timestamp}_scan.log"

    with log_file.open("w", encoding="utf-8") as file:
        file.write(log_stream.getvalue())

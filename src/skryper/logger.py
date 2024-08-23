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


def setup_logger() -> (logging.Logger, StringIO):
    """
    Sets up the logger for the application. Logs are stored in memory and can be written to a file later.

    Returns:
        logging.Logger: Configured logger instance.
        StringIO: Log stream to store logs in memory.
    """
    logger = logging.getLogger("DirectoryScanner")
    logger.setLevel(logging.INFO)

    log_stream = StringIO()
    stream_handler = logging.StreamHandler(log_stream)
    stream_handler.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    # Add a console handler to always log to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger, log_stream


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

    with open(log_file, "w", encoding="utf-8") as file:
        file.write(log_stream.getvalue())

    log_stream.close()

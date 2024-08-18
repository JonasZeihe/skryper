"""
Logger component for the directory scanning application.
"""

import logging
from datetime import datetime
from pathlib import Path


def setup_logger(log_dir: Path = Path(".")) -> logging.Logger:
    """
    Sets up the logger for the application.

    Args:
        log_dir (Path): The directory where the log file will be saved.

    Returns:
        logging.Logger: Configured logger instance.
    """
    log_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"{timestamp}_scan.log"

    logger = logging.getLogger("DirectoryScanner")
    logger.setLevel(logging.INFO)

    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    fh.setFormatter(formatter)

    logger.addHandler(fh)

    return logger

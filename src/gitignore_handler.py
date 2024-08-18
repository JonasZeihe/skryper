"""
Utility functions for handling .gitignore files.
"""

from pathlib import Path
from typing import Set, Optional
import logging


def load_gitignore(path: Path, logger: Optional[logging.Logger] = None) -> Set[str]:
    """
    Loads the .gitignore file and returns a set of ignored paths.

    Args:
        path (Path): The path to the .gitignore file.
        logger (Optional[logging.Logger]): Logger instance for logging.

    Returns:
        Set[str]: A set of paths that are ignored according to the .gitignore rules.
    """
    ignored_paths = set()
    if path.is_file():
        if logger:
            logger.info(f"Loading .gitignore from {path}")
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith("#"):
                    if line.endswith("/"):
                        line = line[:-1]
                    if line.startswith("/"):
                        line = line[1:]
                    ignored_paths.add(line)
                    if logger:
                        logger.debug(f"Adding ignore rule: {line}")
    return ignored_paths


def is_ignored(
    path: Path, ignored_paths: Set[str], logger: Optional[logging.Logger] = None
) -> bool:
    """
    Checks if a given path is ignored based on the .gitignore rules.

    Args:
        path (Path): The path to check.
        ignored_paths (Set[str]): A set of paths that are ignored according to the .gitignore rules.
        logger (Optional[logging.Logger]): Logger instance for logging.

    Returns:
        bool: True if the path is ignored, False otherwise.
    """
    relative_path = str(path)
    for ignored in ignored_paths:
        if ignored in relative_path:
            if logger:
                logger.debug(f"Path {relative_path} is ignored due to rule: {ignored}")
            return True
    if logger:
        logger.debug(f"Path {relative_path} is not ignored")
    return False

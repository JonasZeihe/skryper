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
                original_line = line.strip()
                if original_line and not original_line.startswith("#"):
                    if original_line.endswith("/"):
                        original_line = original_line[:-1]
                    if original_line.startswith("/"):
                        original_line = original_line[1:]
                    ignored_paths.add(original_line)
                    if logger:
                        logger.debug(f"Adding ignore rule: {original_line}")
                        if ".github" in original_line:
                            logger.debug(
                                f"Rule affecting .github found: {original_line}"
                            )
    return ignored_paths


def is_ignored(
    path: Path,
    ignored_paths: Set[str],
    inclusion_rules: Set[str],
    logger: Optional[logging.Logger] = None,
) -> bool:
    """
    Checks if a given path is ignored based on the .gitignore rules,
    but includes paths explicitly listed in inclusion_rules.

    Args:
        path (Path): The path to check.
        ignored_paths (Set[str]): A set of paths that are ignored according to the .gitignore rules.
        inclusion_rules (Set[str]): A set of paths that should be included regardless of .gitignore rules.
        logger (Optional[logging.Logger]): Logger instance for logging.

    Returns:
        bool: True if the path is ignored and not in inclusion_rules, False otherwise.
    """
    relative_path = str(path)
    if logger:
        logger.debug(f"Checking if path '{relative_path}' should be ignored")

    # Check if the path should be included regardless of ignore rules
    for inclusion in inclusion_rules:
        if inclusion in relative_path:
            if logger:
                logger.debug(
                    f"Path '{relative_path}' is included due to rule: {inclusion}"
                )
            return False

    # Otherwise, check if the path should be ignored
    for ignored in ignored_paths:
        if ignored in relative_path:
            if logger:
                logger.debug(
                    f"Path '{relative_path}' is ignored due to rule: {ignored}"
                )
            return True

    if logger:
        logger.debug(f"Path '{relative_path}' is not ignored")

    return False

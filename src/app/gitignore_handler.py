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
Utility functions for handling .gitignore files.
"""

# gitignore_handler.py

from pathlib import Path
from typing import List, Set, Optional
import fnmatch
import logging


def load_gitignore(path: Path, logger: Optional[logging.Logger] = None) -> List[str]:
    """
    Loads the .gitignore file and returns a list of patterns to ignore.

    Args:
        path (Path): Path to the .gitignore file.
        logger (Optional[logging.Logger]): Logger instance for logging.

    Returns:
        List[str]: List of ignore patterns from the .gitignore file.
    """
    ignore_patterns = []
    if path.is_file():
        log_info(logger, f"Loading .gitignore from: {path}")
        ignore_patterns = extract_patterns_from_file(path, logger)
    return ignore_patterns


def extract_patterns_from_file(
    path: Path, logger: Optional[logging.Logger] = None
) -> List[str]:
    """
    Extracts ignore patterns from a .gitignore file.

    Args:
        path (Path): Path to the .gitignore file.
        logger (Optional[logging.Logger]): Logger instance for logging.

    Returns:
        List[str]: Normalized patterns from the file.
    """
    patterns = []
    with path.open("r", encoding="utf-8") as file:
        for line in file:
            clean_pattern = clean_gitignore_line(line)
            if clean_pattern:
                normalized_pattern = normalize_gitignore_pattern(clean_pattern)
                patterns.append(normalized_pattern)
                log_debug(logger, f"Added ignore pattern: {normalized_pattern}")
    return patterns


def clean_gitignore_line(line: str) -> Optional[str]:
    """
    Cleans a line from a .gitignore file by stripping comments and whitespace.

    Args:
        line (str): The line to clean.

    Returns:
        Optional[str]: The cleaned line, or None if it's empty or a comment.
    """
    line = line.strip()
    if line and not line.startswith("#"):
        return line
    return None


def normalize_gitignore_pattern(pattern: str) -> str:
    """
    Normalize .gitignore patterns to ensure consistency in matching.

    Args:
        pattern (str): The pattern from .gitignore to normalize.

    Returns:
        str: The normalized pattern.
    """
    return pattern.rstrip("/").lstrip("/")


def is_ignored(
    path: Path,
    ignore_patterns: List[str],
    inclusion_rules: Set[str],
    logger: Optional[logging.Logger] = None,
) -> bool:
    """
    Checks if a path should be ignored based on .gitignore patterns,
    while considering inclusion rules.

    Args:
        path (Path): The path to check.
        ignore_patterns (List[str]): Patterns from the .gitignore file.
        inclusion_rules (Set[str]): Paths that should be included, regardless of .gitignore rules.
        logger (Optional[logging.Logger]): Logger instance for logging.

    Returns:
        bool: True if the path should be ignored, False otherwise.
    """
    relative_path = str(path).replace("\\", "/")
    log_debug(logger, f"Checking if path '{relative_path}' should be ignored.")

    if relative_path in inclusion_rules:
        log_debug(logger, f"Path explicitly included: {relative_path}")
        return False

    for pattern in ignore_patterns:
        if match_pattern(relative_path, path.name, pattern, logger):
            log_info(
                logger, f"Path ignored: {relative_path} based on pattern: {pattern}"
            )
            return True

    log_debug(logger, f"Path not ignored: {relative_path}")
    return False


def match_pattern(
    relative_path: str,
    file_name: str,
    pattern: str,
    logger: Optional[logging.Logger] = None,
) -> bool:
    """
    Checks if a path or file name matches a given pattern.

    Args:
        relative_path (str): The relative path to check.
        file_name (str): The file name to check.
        pattern (str): The pattern to match against.
        logger (Optional[logging.Logger]): Logger instance for logging.

    Returns:
        bool: True if the pattern matches, False otherwise.
    """
    if fnmatch.fnmatch(relative_path, pattern) or fnmatch.fnmatch(file_name, pattern):
        return True
    return False


def log_info(logger: Optional[logging.Logger], message: str):
    """
    Logs an info-level message if a logger is provided.

    Args:
        logger (Optional[logging.Logger]): Logger instance for logging.
        message (str): The message to log.
    """
    if logger:
        logger.info(message)


def log_debug(logger: Optional[logging.Logger], message: str):
    """
    Logs a debug-level message if a logger is provided.

    Args:
        logger (Optional[logging.Logger]): Logger instance for logging.
        message (str): The message to log.
    """
    if logger:
        logger.debug(message)

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
        if logger:
            logger.info(f"Loading .gitignore from: {path}")
        with path.open("r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith("#"):
                    normalized_pattern = normalize_gitignore_pattern(line)
                    ignore_patterns.append(normalized_pattern)
                    if logger:
                        logger.debug(f"Added ignore pattern: {normalized_pattern}")
    return ignore_patterns


def normalize_gitignore_pattern(pattern: str) -> str:
    """
    Normalize .gitignore patterns to ensure consistency in matching.

    Args:
        pattern (str): The pattern from .gitignore to normalize.

    Returns:
        str: The normalized pattern.
    """
    if pattern.endswith("/"):
        pattern = pattern.rstrip("/")
    if pattern.startswith("/"):
        pattern = pattern.lstrip("/")
    return pattern


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

    if logger:
        logger.debug(
            f"Checking if path '{relative_path}' should be ignored with patterns: {ignore_patterns}"
        )

    if relative_path in inclusion_rules:
        if logger:
            logger.debug(f"Path explicitly included: {relative_path}")
        return False

    for pattern in ignore_patterns:
        if fnmatch.fnmatch(relative_path, pattern) or fnmatch.fnmatch(
            path.name, pattern
        ):
            if logger:
                logger.info(
                    f"Path ignored: {relative_path} based on pattern: {pattern}"
                )
            return True

    if logger:
        logger.debug(f"Path not ignored: {relative_path}")
    return False

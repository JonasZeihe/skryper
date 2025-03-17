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
This module provides functionality to recursively scan directories,
considering .gitignore files and excluding specified files or directories.
"""

# directory_scanner.py

import logging
from pathlib import Path
from .gitignore_handler import load_gitignore, is_ignored


def scan_directory(directory: Path, config, logger: logging.Logger, prefix=""):
    """
    Scans the directory and appends the structure to the config's result,
    considering .gitignore files and excluding specified files or directories.

    Args:
        directory (Path): The directory to scan.
        config: The configuration object that holds ignore rules and results.
        logger (logging.Logger): Logger instance for logging.
        prefix (str, optional): A prefix used for formatting the output. Defaults to an empty string.
    """
    logger.debug(f"Scanning directory: {directory}")

    current_ignore_patterns = update_ignore_patterns(directory, config, logger, prefix)

    entries = sorted(directory.iterdir(), key=lambda e: (e.is_file(), e.name.lower()))
    total_entries = len(entries)

    for index, path in enumerate(entries):
        connector = "└── " if index == total_entries - 1 else "├── "
        relative_path = path.relative_to(directory)

        if is_ignored(
            relative_path, current_ignore_patterns, config.inclusion_rules, logger
        ):
            handle_ignored_path(path, relative_path, config, logger, prefix, connector)
            continue

        if path.is_dir():
            process_directory(
                path, config, logger, prefix, connector, index == total_entries - 1
            )
        else:
            process_file(path, config, logger, prefix, connector)


def update_ignore_patterns(directory: Path, config, logger: logging.Logger, prefix=""):
    """
    Updates the ignore patterns by loading .gitignore files from the directory.

    Args:
        directory (Path): The directory where the .gitignore might be located.
        config: The configuration object that holds the base ignore patterns.
        logger (logging.Logger): Logger instance for logging.
        prefix (str, optional): A prefix used for formatting the output.

    Returns:
        list: Updated list of ignore patterns.
    """
    gitignore_path = directory / ".gitignore"
    current_ignore_patterns = list(config.base_gitignore_paths)

    if gitignore_path.is_file():
        logger.debug(f"Found .gitignore at: {gitignore_path}")
        current_ignore_patterns.extend(load_gitignore(gitignore_path, logger))
        config.result.append(f"{prefix}├── .gitignore")

    return current_ignore_patterns


def process_directory(
    path: Path, config, logger: logging.Logger, prefix, connector, is_last_entry
):
    """
    Processes a directory, appends it to the result, and recursively scans its content.

    Args:
        path (Path): The directory path.
        config: The configuration object that holds the scan result.
        logger (logging.Logger): Logger instance for logging.
        prefix (str): The current prefix used for formatting the output.
        connector (str): The string used to indicate the hierarchy.
        is_last_entry (bool): Indicates whether this is the last entry in the directory.
    """
    config.result.append(f"{prefix}{connector}{path.name}/")
    logger.debug(f"Entering directory: {path}")
    scan_directory(path, config, logger, prefix + ("    " if is_last_entry else "│   "))


def process_file(path: Path, config, logger: logging.Logger, prefix, connector):
    """
    Processes a file, appends it to the result, and handles encoding issues.

    Args:
        path (Path): The file path.
        config: The configuration object that holds the scan result.
        logger (logging.Logger): Logger instance for logging.
        prefix (str): The current prefix used for formatting the output.
        connector (str): The string used to indicate the hierarchy.
    """
    try:
        config.result.append(f"{prefix}{connector}{path.name}")
        logger.info(f"Added file: {path.name}")
    except UnicodeEncodeError:
        safe_name = path.name.encode("utf-8", "replace").decode("utf-8")
        config.result.append(f"{prefix}{connector}{safe_name}")
        logger.warning(f"Unicode issue with file: {path.name}")


def handle_ignored_path(
    path: Path, relative_path, config, logger: logging.Logger, prefix, connector
):
    """
    Handles paths that are ignored based on .gitignore or other rules.

    Args:
        path (Path): The path being ignored.
        relative_path (Path): The relative path of the ignored file or directory.
        config: The configuration object that holds the scan result.
        logger (logging.Logger): Logger instance for logging.
        prefix (str): The current prefix used for formatting the output.
        connector (str): The string used to indicate the hierarchy.
    """
    if path.is_dir():
        config.result.append(f"{prefix}{connector}{path.name}/")
        logger.info(f"Ignored directory indicated: {relative_path}")

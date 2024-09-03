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

from pathlib import Path
from .gitignore_handler import load_gitignore, is_ignored
import logging


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

    gitignore_path = directory / ".gitignore"
    current_ignore_patterns = list(config.base_gitignore_paths)

    if gitignore_path.is_file():
        logger.debug(f"Found .gitignore at: {gitignore_path}")
        current_ignore_patterns.extend(load_gitignore(gitignore_path, logger))
        config.result.append(f"{prefix}├── .gitignore")

    entries = sorted(directory.iterdir(), key=lambda e: (e.is_file(), e.name.lower()))
    total_entries = len(entries)

    for index, path in enumerate(entries):
        relative_path = path.relative_to(directory)

        connector = "└── " if index == total_entries - 1 else "├── "

        if is_ignored(
            relative_path, current_ignore_patterns, config.inclusion_rules, logger
        ):
            if path.is_dir():
                config.result.append(f"{prefix}{connector}{path.name}/")
                logger.info(f"Ignored directory indicated: {relative_path}")
            continue

        if path.is_dir():
            config.result.append(f"{prefix}{connector}{path.name}/")
            logger.debug(f"Entering directory: {path}")
            scan_directory(
                path,
                config,
                logger,
                prefix + ("    " if index == total_entries - 1 else "│   "),
            )
        else:
            try:
                config.result.append(f"{prefix}{connector}{path.name}")
                logger.info(f"Added file: {path.name}")
            except UnicodeEncodeError:
                safe_name = path.name.encode("utf-8", "replace").decode("utf-8")
                config.result.append(f"{prefix}{connector}{safe_name}")
                logger.warning(f"Unicode issue with file: {path.name}")

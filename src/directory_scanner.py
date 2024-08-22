"""
This module provides functionality to recursively scan directories,
considering .gitignore files and excluding specified files or directories.
"""

import logging
from pathlib import Path
import os
from config import DirectoryScannerConfig
from gitignore_handler import load_gitignore, is_ignored


def scan_directory(
    directory: Path,
    config: DirectoryScannerConfig,
    logger: logging.Logger,
    prefix: str = "",
) -> None:
    """
    Recursively scans a directory and records its structure, considering .gitignore files.

    Args:
        directory (Path): The directory to scan.
        config (DirectoryScannerConfig): The configuration for the scan, including excluded files and gitignore paths.
        logger (logging.Logger): Logger instance for logging.
        prefix (str, optional): A prefix used for formatting the output. Defaults to an empty string.
    """
    logger.debug(f"Starting scan of directory: {directory}")

    gitignore_path = directory / ".gitignore"
    current_ignored_paths = config.base_gitignore_paths.copy()

    if gitignore_path.is_file():
        logger.debug(f"Found .gitignore file at: {gitignore_path}")
        current_ignored_paths.update(load_gitignore(gitignore_path, logger))
        config.result.append(prefix + "├── .gitignore")
        logger.info(
            f"Loaded .gitignore in '{directory}' with rules: {current_ignored_paths}"
        )

    entries = sorted(os.listdir(directory))
    logger.debug(f"Directory entries for '{directory}': {entries}")

    for i, entry in enumerate(entries):
        path = directory / entry
        relative_path = path.relative_to(Path.cwd())

        if entry in config.excluded_files:
            logger.info(f"Excluded '{entry}' because it is in the excluded files list")
            continue

        if path.suffix == ".exe":
            logger.info(f"Excluded '{entry}' because it is an executable file")
            continue

        if is_ignored(
            relative_path, current_ignored_paths, config.inclusion_rules, logger
        ):
            logger.info(f"Ignored '{relative_path}' based on .gitignore rules")
            if path.is_dir():
                connector = "└── " if i == len(entries) - 1 else "├── "
                config.result.append(prefix + connector + entry + "/")
            continue

        connector = "└── " if i == len(entries) - 1 else "├── "
        if path.is_dir():
            config.result.append(prefix + connector + entry + "/")
            new_prefix = "    " if i == len(entries) - 1 else "│   "
            logger.debug(f"Recursively scanning directory: {path}")
            scan_directory(path, config, logger, prefix + new_prefix)
        else:
            try:
                config.result.append(prefix + connector + entry)
                logger.info(f"Added file '{entry}'")
            except UnicodeEncodeError:
                safe_entry = entry.encode("utf-8", "replace").decode("utf-8")
                config.result.append(prefix + connector + safe_entry)
                logger.warning(f"Unicode error with file '{entry}'")

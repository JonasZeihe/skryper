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
This module defines the configuration for the directory scanner.

The configuration includes rules for ignoring specific files and directories,
inclusion rules to override ignore patterns, and other settings required 
during the directory scanning process.
"""

# config.py

from dataclasses import dataclass, field
from typing import Set, List


@dataclass
class DirectoryScannerConfig:
    """
    A configuration class for controlling the behavior of the directory scanner.
    """

    base_gitignore_paths: Set[str] = field(default_factory=set)
    excluded_files: Set[str] = field(
        default_factory=lambda: get_default_excluded_files()
    )
    inclusion_rules: Set[str] = field(
        default_factory=lambda: get_default_inclusion_rules()
    )
    output_filename: str = ""
    result: List[str] = field(default_factory=list)


def get_default_excluded_files() -> Set[str]:
    """
    Provides a default set of files and directories to exclude during scanning.

    Returns:
        Set[str]: A set of default excluded files and directories.
    """
    return {"__pycache__", ".git", ".mypy_cache", ".venv"}


def get_default_inclusion_rules() -> Set[str]:
    """
    Provides a default set of files and directories to include, overriding ignore rules.

    Returns:
        Set[str]: A set of default inclusion rules.
    """
    return {".github"}

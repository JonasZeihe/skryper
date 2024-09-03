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
        default_factory=lambda: {"__pycache__", ".git", ".mypy_cache"}
    )
    inclusion_rules: Set[str] = field(default_factory=lambda: {".github"})
    output_filename: str = ""
    result: List[str] = field(default_factory=list)

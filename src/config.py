"""
Configuration for the directory scanner.
"""

from dataclasses import dataclass, field
from typing import Set, List


@dataclass
class DirectoryScannerConfig:
    """
    Configuration for directory scanning.

    Attributes:
        base_gitignore_paths: Paths to gitignore files.
        excluded_files: Files and directories to exclude.
        inclusion_rules: Files and directories to include regardless of .gitignore rules.
        output_filename: Output file name.
        result: Scanning results.
    """

    base_gitignore_paths: Set[str] = field(default_factory=set)
    excluded_files: Set[str] = field(
        default_factory=lambda: {"__pycache__", ".git", ".mypy_cache"}
    )
    inclusion_rules: Set[str] = field(default_factory=lambda: {".github"})
    output_filename: str = ""
    result: List[str] = field(default_factory=list)

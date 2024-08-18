"""
Utility functions for handling .gitignore files.
"""

from pathlib import Path
from typing import Set


def load_gitignore(path: Path) -> Set[str]:
    """
    Loads the .gitignore file and returns a set of ignored paths.

    Args:
        path (Path): The path to the .gitignore file.

    Returns:
        Set[str]: A set of paths that are ignored according to the .gitignore rules.
    """
    ignored_paths = set()
    if path.is_file():
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith("#"):
                    if line.endswith("/"):
                        line = line[:-1]
                    ignored_paths.add(line)
    return ignored_paths


def is_ignored(path: Path, ignored_paths: Set[str]) -> bool:
    """
    Checks if a given path is ignored based on the .gitignore rules.

    Args:
        path (Path): The path to check.
        ignored_paths (Set[str]): A set of paths that are ignored according to the .gitignore rules.

    Returns:
        bool: True if the path is ignored, False otherwise.
    """
    for ignored in ignored_paths:
        if path.match(ignored) or str(path).startswith(ignored):
            return True
    return False

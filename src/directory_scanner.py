from pathlib import Path
import os
from typing import List
from config import DirectoryScannerConfig
from gitignore_handler import load_gitignore, is_ignored


def scan_directory(
    directory: Path, config: DirectoryScannerConfig, prefix: str = ""
) -> None:
    """
    Recursively scans a directory and records its structure, considering .gitignore files.
    """
    gitignore_path = directory / ".gitignore"
    current_ignored_paths = config.base_gitignore_paths.copy()

    if gitignore_path.is_file():
        current_ignored_paths.update(load_gitignore(gitignore_path))
        config.result.append(prefix + "├── .gitignore")

    entries = sorted(os.listdir(directory))
    for i, entry in enumerate(entries):
        path = directory / entry
        relative_path = path.relative_to(Path.cwd())

        if entry in config.excluded_files:
            continue

        if is_ignored(relative_path, current_ignored_paths):
            if entry in {".git", ".mypy_cache"}:
                connector = "└── " if i == len(entries) - 1 else "├── "
                config.result.append(prefix + connector + entry + "/")
            continue

        connector = "└── " if i == len(entries) - 1 else "├── "
        if path.is_dir():
            config.result.append(prefix + connector + entry + "/")
            new_prefix = "    " if i == len(entries) - 1 else "│   "
            scan_directory(path, config, prefix + new_prefix)
        else:
            try:
                config.result.append(prefix + connector + entry)
            except UnicodeEncodeError:
                safe_entry = entry.encode("utf-8", "replace").decode("utf-8")
                config.result.append(prefix + connector + safe_entry)

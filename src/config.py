from dataclasses import dataclass, field
from typing import Set, List


@dataclass
class DirectoryScannerConfig:
    base_gitignore_paths: Set[str] = field(default_factory=set)
    excluded_files: Set[str] = field(
        default_factory=lambda: {"__pycache__", ".git", ".mypy_cache"}
    )
    output_filename: str = ""
    result: List[str] = field(default_factory=list)

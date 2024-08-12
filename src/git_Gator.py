"""
git_gator: A script to generate a directory structure representation
           considering .gitignore files and specific exclusions.
"""

import os
from pathlib import Path
from datetime import datetime


def load_gitignore(path: Path) -> set:
    """
    Loads the .gitignore file and returns a set of ignored paths.

    Args:
        path (Path): Path to the .gitignore file.

    Returns:
        set: A set containing the paths to ignore.
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


def is_ignored(path: Path, ignored_paths: set) -> bool:
    """
    Checks if a given path is ignored based on the .gitignore rules.

    Args:
        path (Path): The path to check.
        ignored_paths (set): The set of ignored paths.

    Returns:
        bool: True if the path is ignored, False otherwise.
    """
    for ignored in ignored_paths:
        if path.match(ignored) or str(path).startswith(ignored):
            return True
    return False


def scan_directory(
    directory: Path, base_gitignore_paths: set, prefix: str = "", output: list = None
) -> list:
    """
    Recursively scans a directory and records its structure, considering .gitignore files.

    Args:
        directory (Path): The directory to scan.
        base_gitignore_paths (set): Set of paths to ignore.
        prefix (str): Prefix for formatting the output.
        output (list): The list to store the directory structure.

    Returns:
        list: The updated directory structure as a list of strings.
    """
    if output is None:
        output = []

    gitignore_path = directory / ".gitignore"
    current_ignored_paths = base_gitignore_paths.copy()

    if gitignore_path.is_file():
        current_ignored_paths.update(load_gitignore(gitignore_path))

        # Add .gitignore to the output
        output.append(prefix + "├── .gitignore")

    entries = sorted(os.listdir(directory))
    for i, entry in enumerate(entries):
        path = directory / entry
        relative_path = path.relative_to(Path.cwd())

        # Skip the git_Gator.exe file
        if entry == "git_Gator.exe":
            continue

        if is_ignored(relative_path, current_ignored_paths):
            if entry in {".git", ".mypy_cache"}:
                connector = "└── " if i == len(entries) - 1 else "├── "
                output.append(prefix + connector + entry + "/")
            continue

        connector = "└── " if i == len(entries) - 1 else "├── "
        if path.is_dir():
            output.append(prefix + connector + entry + "/")
            new_prefix = "    " if i == len(entries) - 1 else "│   "
            scan_directory(path, current_ignored_paths, prefix + new_prefix, output)
        else:
            try:
                output.append(prefix + connector + entry)
            except UnicodeEncodeError:
                safe_entry = entry.encode("utf-8", "replace").decode("utf-8")
                output.append(prefix + connector + safe_entry)

    return output


def main():
    """
    Main function to execute the directory scan and save the structure to a file.
    """
    if os.name == "nt":
        import ctypes
        ctypes.windll.kernel32.SetConsoleOutputCP(65001)

    base_gitignore_paths = load_gitignore(Path(".gitignore"))
    base_gitignore_paths.update({"__pycache__", ".git", ".mypy_cache"})
    result = []
    current_dir_name = Path.cwd().name
    result.append(current_dir_name + "/")
    result = scan_directory(Path.cwd(), base_gitignore_paths, "", result)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"{timestamp}_{current_dir_name}_structure.txt"

    with open(output_filename, "w", encoding="utf-8") as f:
        for line in result:
            f.write(line + "\n")


if __name__ == "__main__":
    main()

"""
Entry point for the directory scanning application.

This module scans the current directory's structure and saves the output to a 
timestamped file.
"""

# main.py

from pathlib import Path
from datetime import datetime
import os
import ctypes
import argparse
from skryper.config import DirectoryScannerConfig
from skryper.directory_scanner import scan_directory
from skryper.gitignore_handler import load_gitignore
from skryper.logger import setup_logger, save_logs_to_file


def parse_arguments():
    """
    Parses command-line arguments.

    Returns:
        Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Skryper - Directory Scanning Tool")
    parser.add_argument(
        "-l", "--logging", action="store_true", help="Enable logging to file"
    )
    return parser.parse_args()


def main():
    """
    Executes the directory scan and saves the structure to a timestamped file.
    """
    if os.name == "nt":
        ctypes.windll.kernel32.SetConsoleOutputCP(65001)

    args = parse_arguments()

    logger, log_stream = setup_logger()
    logger.info("Logger initialized successfully.")

    config = DirectoryScannerConfig()
    gitignore_patterns = load_gitignore(Path(".gitignore"))
    logger.info("Loaded .gitignore patterns: %s", gitignore_patterns)

    config.base_gitignore_paths = set(gitignore_patterns)
    config.base_gitignore_paths.update(config.excluded_files)
    logger.info("Final ignore patterns: %s", config.base_gitignore_paths)

    current_dir_name = Path.cwd().name
    config.result.append(f"{current_dir_name}/")
    logger.info("Starting directory scan in '%s'.", current_dir_name)

    scan_directory(Path.cwd(), config, logger)

    config.output_filename = (
        f"{datetime.now():%Y%m%d_%H%M%S}_{current_dir_name}_structure.txt"
    )

    with Path(config.output_filename).open("w", encoding="utf-8") as f:
        f.write("\n".join(config.result))

    logger.info("Directory structure saved to '%s'.", config.output_filename)
    print(f"Directory structure saved to {config.output_filename}")

    if args.logging:
        save_logs_to_file(log_stream, Path.cwd())
        logger.info("Logs saved successfully.")
        log_stream.close()


if __name__ == "__main__":
    main()

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
    parser.add_argument(
        "--output", type=str, default=None, help="Specify output file name"
    )
    return parser.parse_args()


def initialize_logger(args):
    """
    Initializes the logger based on the command-line arguments.

    Args:
        args: Command-line arguments.

    Returns:
        logger, log_stream: Configured logger and log stream.
    """
    logger, log_stream = setup_logger()
    logger.info("Logger initialized successfully.")
    if args.logging:
        logger.info("Logging to file enabled.")
    return logger, log_stream


def configure_directory_scanner():
    """
    Configures the directory scanner and loads .gitignore patterns.

    Returns:
        DirectoryScannerConfig: Configured directory scanner.
    """
    config = DirectoryScannerConfig()
    gitignore_patterns = load_gitignore(Path(".gitignore"))
    config.base_gitignore_paths = set(gitignore_patterns)
    config.base_gitignore_paths.update(config.excluded_files)
    return config


def generate_output_filename(args, current_dir_name):
    """
    Generates the output filename based on arguments or timestamp.

    Args:
        args: Command-line arguments.
        current_dir_name: The name of the current directory.

    Returns:
        str: The output filename.
    """
    if args.output:
        return args.output
    else:
        return f"{datetime.now():%Y%m%d_%H%M%S}_{current_dir_name}_structure.txt"


def save_directory_structure(config, logger):
    """
    Saves the scanned directory structure to a file.

    Args:
        config: DirectoryScannerConfig containing the scan result.
        logger: The logger instance.
    """
    with Path(config.output_filename).open("w", encoding="utf-8") as f:
        f.write("\n".join(config.result))
    logger.info("Directory structure saved to '%s'.", config.output_filename)
    print(f"Directory structure saved to {config.output_filename}")


def main(args=None):
    """
    Executes the directory scan and saves the structure to a timestamped file.
    """
    if args is None:
        args = parse_arguments()

    if os.name == "nt":
        ctypes.windll.kernel32.SetConsoleOutputCP(65001)

    logger, log_stream = initialize_logger(args)
    config = configure_directory_scanner()

    current_dir_name = Path.cwd().name
    config.result.append(f"{current_dir_name}/")
    logger.info("Starting directory scan in '%s'.", current_dir_name)

    scan_directory(Path.cwd(), config, logger)

    config.output_filename = generate_output_filename(args, current_dir_name)
    save_directory_structure(config, logger)

    if args.logging:
        save_logs_to_file(log_stream, Path.cwd())
        log_stream.close()


if __name__ == "__main__":
    main()

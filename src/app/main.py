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

This module scans the structure of subdirectories relative to the executable location
or a given root, and saves the output and logs to timestamped files.
"""

# main.py

from pathlib import Path
from datetime import datetime
import os
import sys
import ctypes
import argparse
from app.config import DirectoryScannerConfig
from app.directory_scanner import scan_directory
from app.gitignore_handler import load_gitignore
from app.logger import setup_logger, save_logs_to_file


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
    parser.add_argument("--root", type=str, default=None, help="Root directory to scan")
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


def generate_output_and_log_filenames(args, current_dir_name):
    """
    Generates filenames for the structure and log files based on arguments or timestamp.

    Args:
        args: Command-line arguments.
        current_dir_name: The name of the current directory.

    Returns:
        tuple: (structure_filename, log_filename)
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    structure_filename = args.output or f"{timestamp}_{current_dir_name}_structure.txt"
    log_filename = f"{timestamp}_scan.log"
    return structure_filename, log_filename


def save_directory_structure(config, logger, output_path):
    """
    Saves the scanned directory structure to a file.

    Args:
        config: DirectoryScannerConfig containing the scan result.
        logger: The logger instance.
        output_path (Path): Full path to the structure output file.
    """
    with output_path.open("w", encoding="utf-8") as f:
        f.write("\n".join(config.result))
    logger.info("Directory structure saved to '%s'.", output_path)
    print(f"Directory structure saved to {output_path}")


def save_log_file(log_stream, output_filename, base_path):
    """
    Saves the in-memory log to a file with the same timestamp as the structure file.

    Args:
        log_stream (StringIO): In-memory log stream.
        output_filename (str): Name of the structure output file.
        base_path (Path): Directory where the log file will be saved.
    """
    log_filename = output_filename.replace("_structure.txt", "_scan.log")
    log_path = base_path / log_filename
    save_logs_to_file(log_stream, log_path)


def main(args=None):
    """
    Executes the directory scan and saves the structure and logs to files.
    """
    if args is None:
        args = parse_arguments()

    if os.name == "nt":
        ctypes.windll.kernel32.SetConsoleOutputCP(65001)

    logger, log_stream = initialize_logger(args)
    config = configure_directory_scanner()

    execution_dir = (
        Path(args.root) if args.root else Path(os.path.dirname(sys.executable))
    )
    current_dir_name = execution_dir.name
    config.result.append(f"{current_dir_name}/")
    logger.info("Starting directory scan in '%s'.", execution_dir)

    scan_directory(execution_dir, config, logger)

    structure_filename, log_filename = generate_output_and_log_filenames(
        args, current_dir_name
    )
    structure_path = execution_dir / structure_filename
    log_path = execution_dir / log_filename

    config.output_filename = structure_filename
    save_directory_structure(config, logger, structure_path)

    if args.logging:
        log_filename = config.output_filename.replace("_structure.txt", "_log.txt")
        log_path = execution_dir / log_filename
        save_logs_to_file(log_stream, log_path)
        log_stream.close()


if __name__ == "__main__":
    main()

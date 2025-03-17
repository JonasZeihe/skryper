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
Integration test for the Skryper directory scanning application.

This test verifies that the correct files are included or excluded based on .gitignore rules
and that the application behaves as expected.
"""

# test_skryper.py

import pytest
import sys
import glob
import os
from pathlib import Path
from unittest.mock import patch
from app.main import main
from app.logger import save_logs_to_file, setup_logger


@pytest.fixture(scope="function")
def test_environment(tmp_path):
    """
    Creates a temporary test environment with necessary test files and directories.

    Args:
        tmp_path (Path): Temporary directory provided by pytest.

    Returns:
        Path: The path to the created test environment.
    """
    test_dir = tmp_path / "test_environment"
    test_dir.mkdir()

    (test_dir / "file1.txt").write_text("This is a test file.")
    (test_dir / "file2.log").write_text("This is a log file.")
    (test_dir / "file3.exe").write_text("This is an executable file.")

    ignored_dir = test_dir / "ignored_dir"
    ignored_dir.mkdir()
    (ignored_dir / "file4.txt").write_text("This file should be ignored.")

    nested_dir = test_dir / "nested"
    nested_dir.mkdir()
    (nested_dir / "included_file.txt").write_text("This file should be included.")
    (nested_dir / "ignored_file.txt").write_text("This file should be ignored.")

    subnested_dir = nested_dir / "subnested"
    subnested_dir.mkdir()
    (subnested_dir / "file5.txt").write_text("This file should be included.")
    (subnested_dir / "file6.log").write_text("This log file should be ignored.")

    (test_dir / ".gitignore").write_text("*.log\n/ignored_dir/\n/subdir/\n*.exe\n")
    (nested_dir / ".gitignore").write_text("ignored_file.txt\n")

    yield test_dir


def test_integration(test_environment, monkeypatch):
    """
    Runs an integration test for the directory scanning application.

    Args:
        test_environment (Path): Path to the test environment.
        monkeypatch (pytest.MonkeyPatch): Pytest utility to modify attributes during testing.
    """
    monkeypatch.setattr(sys, "argv", ["main.py", "--output", "output.txt"])
    os.chdir(test_environment)

    main()

    output_file = test_environment / "output.txt"
    assert output_file.exists(), "Output file was not created."

    with output_file.open("r", encoding="utf-8") as f:
        result = f.read()

    assert "file1.txt" in result
    assert "included_file.txt" in result
    assert "file5.txt" in result

    assert "file2.log" not in result
    assert "file3.exe" not in result
    assert "ignored_file.txt" not in result
    assert "file6.log" not in result


def test_logger_integration(test_environment):
    """
    Tests whether the logger correctly logs messages and saves them to a file.

    Args:
        test_environment (Path): Path to the test environment.
    """
    logger, log_stream = setup_logger()

    logger.info("Test log entry for logger.")
    log_content = log_stream.getvalue()
    assert "Test log entry for logger." in log_content

    save_logs_to_file(log_stream, log_dir=test_environment)
    log_files = list(test_environment.glob("*_scan.log"))
    assert len(log_files) > 0, "No log file was created."

    with log_files[0].open("r", encoding="utf-8") as f:
        file_content = f.read()

    assert "Test log entry for logger." in file_content

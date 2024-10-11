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

import sys
import unittest
from unittest.mock import patch
from pathlib import Path
import os
import shutil
from skryper.main import main
from skryper.logger import save_logs_to_file, setup_logger
import glob


class TestSkryper(unittest.TestCase):
    """Test suite for the Skryper directory scanning application, including Logger testing."""

    def setUp(self):
        """Set up the test environment."""
        self.test_dir = Path("test_environment")
        self.test_dir.mkdir(exist_ok=True)

        self.create_test_files()

        (self.test_dir / ".gitignore").write_text(
            "*.log\n/ignored_dir/\n/subdir/\n*.exe\n"
        )
        (self.test_dir / "nested" / ".gitignore").write_text("ignored_file.txt\n")

        self.create_complex_structure()

        self.original_cwd = Path.cwd()
        os.chdir(self.test_dir)

        self.logger, self.log_stream = setup_logger()

    def create_test_files(self):
        """Helper function to create a set of test files and directories."""
        (self.test_dir / "file1.txt").write_text("This is a test file.")
        (self.test_dir / "file2.log").write_text("This is a log file.")
        (self.test_dir / "file3.exe").write_text("This is an executable file.")
        (self.test_dir / "ignored_dir").mkdir(exist_ok=True)
        (self.test_dir / "ignored_dir" / "file4.txt").write_text(
            "This file should be ignored."
        )
        (self.test_dir / "nested").mkdir(exist_ok=True)
        (self.test_dir / "nested" / "included_file.txt").write_text(
            "This file should be included."
        )
        (self.test_dir / "nested" / "ignored_file.txt").write_text(
            "This file should be ignored."
        )
        (self.test_dir / "nested" / "subnested").mkdir(exist_ok=True)
        (self.test_dir / "nested" / "subnested" / "file5.txt").write_text(
            "This file should be included."
        )
        (self.test_dir / "nested" / "subnested" / "file6.log").write_text(
            "This log file should be ignored."
        )
        (self.test_dir / "subdir").mkdir(exist_ok=True)
        (self.test_dir / "subdir" / "file7.txt").write_text(
            "This file should be ignored."
        )
        (self.test_dir / "subdir" / "another_ignored_dir").mkdir(exist_ok=True)
        (self.test_dir / "subdir" / "another_ignored_dir" / "file8.txt").write_text(
            "This file should also be ignored."
        )

    def create_complex_structure(self):
        """Helper function to create a complex nested structure."""
        (self.test_dir / "complex").mkdir(exist_ok=True)
        (self.test_dir / "complex" / "deep").mkdir(exist_ok=True)
        (self.test_dir / "complex" / "deep" / "file9.txt").write_text(
            "This deep file should be included."
        )
        (self.test_dir / "complex" / "deep" / "file10.log").write_text(
            "This deep log file should be ignored."
        )

    def tearDown(self):
        """Tear down the test environment."""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)

    def test_integration(self):
        """Run the integration test for the directory scanning application."""
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")

        with patch.object(sys, "argv", ["main.py", "--output", "output.txt"]):
            main()

        output_file = Path("output.txt")
        self.assertTrue(output_file.exists(), "Output file was not created.")

        with output_file.open("r", encoding="utf-8") as f:
            result = f.read()

        self.assertIn("file1.txt", result)
        self.assertIn("included_file.txt", result)
        self.assertIn("file5.txt", result)
        self.assertIn("file9.txt", result)

        self.assertNotIn("file2.log", result)
        self.assertNotIn("file3.exe", result)
        self.assertNotIn("ignored_file.txt", result)
        self.assertNotIn("file7.txt", result)
        self.assertNotIn("another_ignored_dir", result)
        self.assertNotIn("file10.log", result)

        self.assertIn("ignored_dir/", result)
        self.assertNotIn("ignored_dir/file4.txt", result)

    def test_logger_integration(self):
        """Test if the logger writes logs to the in-memory stream and saves to a file."""
        self.logger.info("Test log entry for logger.")

        log_content = self.log_stream.getvalue()
        self.assertIn("Test log entry for logger.", log_content)

        save_logs_to_file(self.log_stream, log_dir=self.test_dir)

        log_files = glob.glob(f"{self.test_dir}/*_scan.log")
        self.assertTrue(len(log_files) > 0, "No log file was created.")
        log_file = Path(log_files[0])

        with log_file.open("r", encoding="utf-8") as f:
            file_content = f.read()

        self.assertIn("Test log entry for logger.", file_content)

        log_file.unlink()


if __name__ == "__main__":
    unittest.main()

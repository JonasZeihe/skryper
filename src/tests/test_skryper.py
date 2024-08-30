"""
Integration test for the Skryper directory scanning application.

This test verifies that the correct files are included or excluded based on .gitignore rules
and that the application behaves as expected.
"""

import sys
import unittest
from unittest.mock import patch
from pathlib import Path
import os
import shutil
from skryper.main import main


class TestSkryper(unittest.TestCase):
    """Test suite for the Skryper directory scanning application."""

    def setUp(self):
        """Set up the test environment."""
        self.test_dir = Path("test_environment")
        self.test_dir.mkdir(exist_ok=True)

        # Create a variety of test files and directories
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

        (self.test_dir / ".gitignore").write_text(
            "*.log\n/ignored_dir/\n/subdir/\n*.exe\n"
        )
        (self.test_dir / "nested" / ".gitignore").write_text("ignored_file.txt\n")

        # Add a more complex nested structure
        (self.test_dir / "complex").mkdir(exist_ok=True)
        (self.test_dir / "complex" / "deep").mkdir(exist_ok=True)
        (self.test_dir / "complex" / "deep" / "file9.txt").write_text(
            "This deep file should be included."
        )
        (self.test_dir / "complex" / "deep" / "file10.log").write_text(
            "This deep log file should be ignored."
        )

        self.original_cwd = Path.cwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        """Tear down the test environment."""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)

    def test_integration(self):
        """Run the integration test for the directory scanning application."""
        # Set stdout encoding to UTF-8
        sys.stdout.reconfigure(encoding="utf-8")

        with patch.object(sys, "argv", ["main.py", "--output", "output.txt"]):
            main()

        output_file = Path("output.txt")
        self.assertTrue(output_file.exists(), "Output file was not created.")

        with output_file.open("r", encoding="utf-8") as f:
            result = f.read()

        # Verify included files
        self.assertIn("file1.txt", result)
        self.assertIn("included_file.txt", result)
        self.assertIn("file5.txt", result)
        self.assertIn("file9.txt", result)

        # Verify ignored files
        self.assertNotIn("file2.log", result)
        self.assertNotIn("file3.exe", result)
        self.assertNotIn("ignored_file.txt", result)
        self.assertNotIn("file7.txt", result)
        self.assertNotIn("another_ignored_dir", result)
        self.assertNotIn("file10.log", result)

        # Verify directories are correctly scanned or ignored
        self.assertIn("ignored_dir/", result)
        self.assertNotIn("ignored_dir/file4.txt", result)


if __name__ == "__main__":
    unittest.main()

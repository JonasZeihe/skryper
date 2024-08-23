import unittest
from pathlib import Path
import os
import shutil
from skryper.main import main


class TestSkryper(unittest.TestCase):
    """
    Integration test for the Skryper directory scanning application.
    """

    def setUp(self):
        """
        Set up a test environment before each test.
        Creates a temporary directory with test files and .gitignore files.
        """
        self.test_dir = Path("test_environment")
        self.test_dir.mkdir(exist_ok=True)

        (self.test_dir / "file1.txt").write_text("This is a test file.")
        (self.test_dir / "file2.log").write_text("This is a log file.")
        (self.test_dir / "file4.exe").write_text("This is an executable.")

        (self.test_dir / "ignored_dir").mkdir(exist_ok=True)
        (self.test_dir / "ignored_dir" / "file3.txt").write_text(
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
        (self.test_dir / "nested" / "subnested" / "file4.txt").write_text(
            "This file should be included."
        )
        (self.test_dir / "nested" / "subnested" / "file5.log").write_text(
            "This log should be ignored."
        )

        (self.test_dir / "subdir").mkdir(exist_ok=True)
        (self.test_dir / "subdir" / "file6.txt").write_text(
            "This file should be ignored."
        )
        (self.test_dir / "subdir" / "another_ignored_dir").mkdir(exist_ok=True)
        (self.test_dir / "subdir" / "another_ignored_dir" / "file7.txt").write_text(
            "This file should also be ignored."
        )

        (self.test_dir / ".gitignore").write_text(
            "*.log\n/ignored_dir/\n/subdir/\n*.exe"
        )
        (self.test_dir / "nested" / ".gitignore").write_text("ignored_file.txt")

        self.original_cwd = Path.cwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        """
        Clean up the test environment after each test.
        Deletes the temporary directory and its contents.
        """
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)

    def test_integration(self):
        """
        Run the main function of the Skryper application
        and verify that the output is as expected.
        """
        main()

        output_files = list(Path(".").glob("*.txt"))
        self.assertTrue(len(output_files) > 0, "Output file was not created.")

        output_file = output_files[0]
        with open(output_file, "r", encoding="utf-8") as f:
            result = f.read()

        self.assertIn("file1.txt", result)
        self.assertNotIn("file2.log", result)
        self.assertNotIn("file4.exe", result)
        self.assertNotIn("ignored_dir/", result)
        self.assertIn("nested/included_file.txt", result)
        self.assertNotIn("nested/ignored_file.txt", result)
        self.assertIn("nested/subnested/file4.txt", result)
        self.assertNotIn("nested/subnested/file5.log", result)
        self.assertNotIn("subdir/", result)

        log_files = list(Path(".").glob("*.log"))
        self.assertTrue(len(log_files) > 0, "Log file was not created.")


if __name__ == "__main__":
    unittest.main()

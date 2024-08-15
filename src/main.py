from pathlib import Path
from datetime import datetime
import os
import ctypes
from config import DirectoryScannerConfig
from directory_scanner import scan_directory
from gitignore_handler import load_gitignore


def main():
    """
    Main function to execute the directory scan and save the structure to a file.
    """
    if os.name == "nt":
        ctypes.windll.kernel32.SetConsoleOutputCP(65001)

    config = DirectoryScannerConfig()
    config.base_gitignore_paths = load_gitignore(Path(".gitignore"))
    config.base_gitignore_paths.update(config.excluded_files)

    current_dir_name = Path.cwd().name
    config.result.append(current_dir_name + "/")

    scan_directory(Path.cwd(), config)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    config.output_filename = f"{timestamp}_{current_dir_name}_structure.txt"

    with open(config.output_filename, "w", encoding="utf-8") as f:
        for line in config.result:
            f.write(line + "\n")

    print(f"Directory structure saved to {config.output_filename}")


if __name__ == "__main__":
    main()

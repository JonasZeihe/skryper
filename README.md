Hier ist eine erweiterte Version der README-Datei mit Tags, die das Projekt besser auffindbar machen:

---

# Skryper

![Skryper Logo](./images/skryper_logo.png)
![Python](https://img.shields.io/badge/python-3.x-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/jonaszeihe/skryper)
![Platform](https://img.shields.io/badge/platform-windows-lightgrey.svg)
![AI-Aided Development](https://img.shields.io/badge/AI--aided%20development-practice%20driven-orange.svg)

**Skryper** is a powerful tool designed to help developers efficiently scan, analyze, and organize their project's file structure while respecting `.gitignore` exclusions. The goal of Skryper is to provide developers with a streamlined way to maintain control over their project files, ensuring that only the relevant files are managed and tracked.

In the often chaotic world of development, managing files can become cumbersome, especially in large projects with multiple contributors. Skryper steps in to simplify this process, offering a clean and clear view of the file landscape. By focusing on files that matter and excluding those that don't, Skryper aids in creating a more organized and manageable codebase.

Skryper isn't just about scanning directories; it's about enhancing your workflow, reducing clutter, and ensuring that your version control system remains clean and precise. This tool reflects the philosophy of clean code management and efficient project organization, helping developers focus on what truly matters: writing and maintaining quality code.

## Technical Overview

Skryper was developed to conduct an in-depth analysis of directory structures, identifying all files relevant to a project. The tool considers `.gitignore` files to ensure that only files not excluded by these rules are scanned. This approach allows for more precise file management and better project visibility.

### Key Features

- **Directory Scanning**: Traverses specified directories and lists all relevant files.
- **Respect for `.gitignore`**: Automatically ignores files excluded by `.gitignore` files.
- **Logging**: Generates detailed logs, enabling users to trace the scanning process and review the identified files.

## Installation

1. **Download**

   - Go to [GitHub Releases](https://github.com/jonaszeihe/skryper/releases) and download the latest version of Skryper.

2. **Installation Instructions**

   - Download the release and extract it to a directory of your choice.
   - Ensure that Python 3.x is installed on your system. If not, download it from [python.org](https://www.python.org/).

3. **Install Dependencies**
   - Install all necessary Python dependencies with the following command:
     ```bash
     pip install -r requirements.txt
     ```

## Development

If you are interested in contributing to Skryper or wish to modify it for your own purposes, you can set up a development environment by following these steps:

1. **Clone the Repository**

   - Clone the Skryper repository from GitHub:
     ```bash
     git clone https://github.com/jonaszeihe/skryper.git
     cd skryper
     ```

2. **Create a Virtual Environment**

   - It is recommended to create a virtual environment to manage dependencies:
     ```bash
     python -m venv venv
     source venv/bin/activate  # On Windows use `venv\Scripts\activate`
     ```

3. **Install Development Dependencies**

   - Install the dependencies required for development:
     ```bash
     pip install -r requirements.txt
     ```

4. **Run Skryper in Development Mode**

   - You can now run Skryper directly from the source code for testing and development:
     ```bash
     python src/main.py --dir /path/to/your/project
     ```

5. **Build the Executable**
   - To build the executable for Skryper, use PyInstaller:
     ```bash
     pyinstaller --name skryper --onefile --specpath src --noconfirm src/main.py
     ```
   - This will generate a standalone executable in the `dist/` directory.

## Integration with Structra

Skryper is designed to work seamlessly with [Structra](https://github.com/JonasZeihe/structra), another tool available on my GitHub profile. Structra takes the file structure generated by Skryper and visualizes it, providing a comprehensive view of your project's architecture. This integration enhances your ability to understand and manage complex project structures.

## AI-Aided Development

Skryper is an example of AI-aided software design and best practice coding. The entire development process was guided by lints and best practices, ensuring a high-quality codebase. While Skryper does not include automated tests, this decision was intentional to better capture the real-world complexities of file structures and `.gitignore` rules in a development environment.

## License

Skryper is licensed under the MIT License. For more details, please see the [LICENSE](./LICENSE) file.

---

With Skryper, you maintain control over your project structure, optimize your workflow, and ensure that no important files are overlooked. Skryper is your sharp eye in the jungle of file structures.

## Tags

- **File Structure Analysis**
- **Directory Scanning**
- **.gitignore Management**
- **Python Tool**
- **Windows Tool**
- **AI-Aided Development**
- **Best Practice Coding**
- **Project Organization**
- **Workflow Optimization**
- **Structra Integration**

---

Diese Tags und die zusätzlichen Abschnitte über die Integration mit Structra und AI-aided Development machen das Projekt leichter auffindbar und geben potenziellen Nutzern und Mitwirkenden einen klaren Überblick über die Ziele und Funktionen von Skryper.

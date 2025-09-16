# Skryper

![Skryper Logo](./images/skryper_logo.png)  
![Python](https://img.shields.io/badge/python-3.x-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/jonaszeihe/skryper)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS-lightgrey.svg)
![Logging Available](https://img.shields.io/badge/logging-optional-brightgreen.svg)
![AI-Aided Development](https://img.shields.io/badge/AI--aided%20development-practice--driven-orange.svg)

> **Skryper** is a cross-platform, open-source **project structure scanner**.  
> It automatically generates a clean **directory tree** of your codebase, fully respecting `.gitignore` rules.  
> Ideal for **Next.js, Python, Node.js, monorepos, or any large project** where clarity and organization matter.

---

## Why Skryper?

Keeping a **codebase organized** is difficult in larger, collaborative projects.  
Existing tools like `tree` or ad-hoc scripts are limited:

- They don’t respect `.gitignore` rules.
- They produce cluttered, inconsistent output.
- They aren’t optimized for **developer workflows**.

**Skryper solves this**: it produces a **clear, standardized, `.gitignore`-aware project tree** that’s perfect for documentation, onboarding, reviews, or integration with other tools like [Structra](https://github.com/JonasZeihe/structra).

---

## Example Output

Here’s Skryper scanning its own repository:

```
skryper/
├── .gitignore
├── .git/
├── .github/
│   └── workflows/
│       └── build.yml
├── .pytest_cache/
├── build/
├── dist/
├── images/
│   ├── skryper.ico
│   └── skryper_logo.png
├── scripts/
│   ├── logic/
│   │   ├── build_app.py
│   │   ├── extract_codebase.py
│   │   ├── init_project.py
│   │   ├── run_logic.py
│   │   ├── test_all.py
│   │   └── update_requirements.py
│   ├── mac/
│   │   ├── 01INIT.command
│   │   ├── build.command
│   │   ├── deactivate_venv.command
│   │   ├── init_project.command
│   │   ├── run.command
│   │   ├── run_extract_codebase.command
│   │   ├── test.command
│   │   └── update_requirements.command
│   ├── windows/
│   │   ├── build.bat
│   │   ├── deactivate_venv.bat
│   │   ├── init_project.bat
│   │   ├── run.bat
│   │   ├── test.bat
│   │   └── update_requirements.bat
│   └── .DS_Store
├── src/
│   ├── app/
│   │   ├── __pycache__/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── directory_scanner.py
│   │   ├── gitignore_handler.py
│   │   ├── logger.py
│   │   └── main.py
│   └── tests/
│       ├── __pycache__/
│       ├── __init__.py
│       └── test_skryper.py
├── venv/
├── LICENSE
├── README.md
├── requirements.txt
├── skryper
└── skryper.code-workspace
```

## ✨ Key Features

- **Directory Scanning** – Recursively builds a clean tree of your project.
- **`.gitignore` Compliance** – Automatically excludes ignored files/folders.
- **Cross-Platform** – Works on **Windows** and **macOS**.
- **Optional Logging** – Enable detailed logs for debugging and auditing.
- **Codebase Documentation** – Perfect for READMEs, onboarding, or architecture reviews.
- **AI-Aided Development** – Built with AI-guided best practices.

---

## 🚀 Installation & Usage

Download the latest binary from [GitHub Releases](https://github.com/jonaszeihe/skryper/releases).

### Windows

```powershell
Skryper_YYYY-MM-DD_HH-MM-SS.exe --logging
```

(Or simply double-click to run)

### macOS

```bash
xattr -rd com.apple.quarantine ./skryper_<timestamp>
./skryper_<timestamp> --logging
```

---

## 🛠 Local Development & Scripts

Run locally with Python:

```bash
python scripts/logic/init_project.py
```

Platform launchers are included:

- **Windows:** `scripts\windows\init_project.bat`
- **macOS:** `./scripts/mac/init_project.command`

Extract a **merged full codebase output**:

```bash
python scripts/logic/extract_codebase.py optional_suffix
```

---

## 🔗 Integration with Structra

Skryper works seamlessly with [Structra](https://github.com/JonasZeihe/structra), which visualizes Skryper’s output for a full **architecture view** of your project.

---

## 🤝 Contributing

1. Clone the repository:

   ```bash
   git clone https://github.com/jonaszeihe/skryper.git
   cd skryper
   ```

2. Install dependencies: `pip install -r requirements.txt`
3. Submit PRs, issues, or feature requests.

---

## 🐞 Reporting Issues

Found a bug? Please [open an issue](https://github.com/jonaszeihe/skryper/issues).
Use the logging option for detailed debugging output.

---

## 📜 License

Licensed under the [MIT License](./LICENSE).

---

## 🔍 Discoverability Tags

Skryper is especially useful for:

- **Project Tree Generator**
- **File Structure Analysis**
- **Project File Tree**
- **Directory Scanning**
- **.gitignore-Aware Project Tree**
- **Git Project Tree Visualization**
- **Codebase Documentation**
- **Cross-Platform Developer Tooling**
- **Python CLI Utility**
- **Logging & Auditing**
- **Architecture & Codebase Visualization**
- **Project Organization & Maintenance**
- **Automation for Codebase Management**
- **Structra Integration**
- **Software Engineering Best Practices**
- **Open Source MIT License**

#!/usr/bin/env python
# (C) 2025 Jonas Zeihe, MIT License. Developer: Jonas Zeihe. Contact: JonasZeihe@gmail.com

import os
import sys
import platform
import subprocess
import shutil


DEV_MODULES = ["pytest", "coverage", "pipreqsnb"]


def main():
    """
    Initialize Python project environment:
    - Create virtual environment
    - Install and upgrade pip and wheel from PyPI
    - Install development modules
    - Generate and install requirements
    - Ensure tkinter availability on macOS
    - Freeze final dependencies
    """
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    os.chdir(root)

    if not os.path.isdir("venv"):
        print("Creating virtual environment...")
        _run([sys.executable, "-m", "venv", "venv"])
    else:
        print("Virtual environment already exists.")

    print("Upgrading pip and wheel in virtual environment...")
    _run_in_venv(["python", "-m", "pip", "install", "--upgrade", "pip", "wheel"])

    for module in DEV_MODULES:
        if not _has_module(module):
            print(f"Installing missing dev dependency: {module}...")
            _run_in_venv(["pip", "install", module])

    print("Generating requirements.txt with pipreqsnb (ignoring venv)...")
    _run_in_venv_cmd("pipreqsnb . --force --ignore venv")

    if os.path.isfile("requirements.txt"):
        print("Installing from requirements.txt...")
        _run_in_venv(["pip", "install", "--no-cache-dir", "-r", "requirements.txt"])

    if platform.system() == "Darwin" and not _has_tkinter():
        print("tkinter not found, attempting brew install python-tk...")
        _maybe_brew_install_tk()

    print("Ensuring clean PyPI wheel...")
    _run_in_venv(["pip", "install", "--force-reinstall", "wheel"])

    print("Freezing final requirements.txt...")
    _run_in_venv(["pip", "freeze"], output="requirements.txt")

    print("Initialization complete.")


def _run(cmd, check=True):
    """
    Execute a subprocess command with optional check.
    """
    if cmd[0] == "python":
        cmd[0] = sys.executable
    subprocess.run(cmd, check=check)


def _run_in_venv(cmd, output=None):
    """
    Execute a command inside the virtual environment.
    Optionally redirect output to a file.
    """
    if cmd[0] == "python":
        cmd[0] = sys.executable

    if (
        "pip" in cmd
        and "install" in cmd
        and platform.system() == "Darwin"
        and "--break-system-packages" not in cmd
    ):
        cmd.append("--break-system-packages")

    if os.name == "nt":
        act = os.path.join("venv", "Scripts", "activate.bat")
        full_cmd = f'call "{act}" && ' + " ".join(cmd)
    else:
        act = "./venv/bin/activate"
        full_cmd = f'. "{act}" && ' + " ".join(cmd)

    if output:
        full_cmd += f" > {output}"

    subprocess.run(full_cmd, shell=True, check=True)


def _run_in_venv_cmd(cmd_str):
    """
    Execute a raw command string inside the virtual environment.
    """
    if os.name == "nt":
        act = os.path.join("venv", "Scripts", "activate.bat")
        full_cmd = f'call "{act}" && {cmd_str}'
    else:
        act = "./venv/bin/activate"
        full_cmd = f'. "{act}" && {cmd_str}'
    subprocess.run(full_cmd, shell=True, check=True)


def _has_module(mod):
    """
    Check if a module can be imported in the virtual environment.
    """
    try:
        _run_in_venv(["python", "-c", f"import {mod}"])
        return True
    except subprocess.CalledProcessError:
        return False


def _has_tkinter():
    """
    Check if tkinter is available in the environment.
    """
    try:
        _run_in_venv_cmd('python -c "import tkinter"')
        return True
    except subprocess.CalledProcessError:
        return False


def _maybe_brew_install_tk():
    """
    Attempt to install tkinter via Homebrew and adjust venv env vars.
    """
    if shutil.which("brew") is None:
        print("Homebrew not found. Can't install tkinter via brew.")
        return

    _run(["brew", "install", "python-tk"])

    act = os.path.join("venv", "bin", "activate")
    with open(act, "a", encoding="utf-8") as f:
        f.write('\nexport PATH="/opt/homebrew/opt/tcl-tk/bin:$PATH"\n')
        f.write('export LDFLAGS="-L/opt/homebrew/opt/tcl-tk/lib"\n')
        f.write('export CPPFLAGS="-I/opt/homebrew/opt/tcl-tk/include"\n')
        f.write('export PKG_CONFIG_PATH="/opt/homebrew/opt/tcl-tk/lib/pkgconfig"\n')

    _run_in_venv_cmd('python -c "import tkinter"')


if __name__ == "__main__":
    main()

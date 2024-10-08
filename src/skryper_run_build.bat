@echo off
REM -----------------------------------------------------------------------------
REM Skryper - A tool to scan, analyze, and organize your project file structures
REM 
REM Copyright (c) 2024 Jonas Zeihe
REM Licensed under the MIT License. See LICENSE file in the project root for details.
REM 
REM Project URL: https://github.com/jonaszeihe/skryper
REM Contact: JonasZeihe@gmail.com
REM -----------------------------------------------------------------------------

pyinstaller --onefile --name skryper --specpath . --clean skryper/main.py

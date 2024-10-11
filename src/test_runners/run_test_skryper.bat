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

@echo off
cls

REM Set the working directory to the project root (one level above the test_runners folder)
cd /d %~dp0..\

REM Running test_skryper.py with coverage
echo Running test_skryper.py with coverage...
coverage run --source=skryper -m unittest tests.test_skryper
coverage report -m

REM Pause to keep the window open until the user presses a key
echo.
echo Press any key to exit...
pause > nul

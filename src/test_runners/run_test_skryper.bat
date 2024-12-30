@echo off
REM -----------------------------------------------------------------------------
REM Skryper - A tool to scan, analyze, and organize your project file structures
REM 
REM Copyright (c) 2024 Jonas Zeihe
REM Licensed under the MIT License. See LICENSE file in the project root for details.
REM 
REM Project URL: https://github.com/jonaszeihe/skryper
REM Contact: JonasZeihe@gmail.com
REM ----------------------------------------------------------------------

REM Activate the virtual environment
call ..\venv\Scripts\activate

REM Set the working directory to the project root
cd /d %~dp0..\

REM Run the specified test with coverage
echo Running test_skryper.py with coverage...
coverage run --source=skryper -m unittest tests.test_skryper
coverage report -m

REM Inform the user
echo.
echo Test execution complete. Review the results above.
echo Press any key to deactivate the virtual environment and exit...
pause > nul

REM Deactivate the virtual environment
deactivate

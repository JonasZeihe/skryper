@echo off
REM ----------------------------------------------------------------------
REM Universal Test Runner - Run Specific Test
REM Executes a specific test in the project for development purposes.
REM 
REM Copyright (c) 2024 Jonas Zeihe
REM Licensed under the MIT License. See LICENSE file in the project root for details.
REM 
REM Project URL: https://github.com/jonaszeihe/skryper
REM Contact: JonasZeihe@gmail.com
REM ----------------------------------------------------------------------

REM Activate the virtual environment
call ..\venv\Scripts\activate


REM Run the specified test
echo Running the specified test...
python -m unittest tests.test_skryper

REM Inform the user
echo.
echo Test execution complete. Review the results above.
echo Press any key to deactivate the virtual environment and exit...
pause > nul

REM Deactivate the virtual environment
deactivate

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

REM Activate the virtual environment
call ..\venv\Scripts\activate

REM Start the build process
echo Building the Skryper executable...
pyinstaller --onefile --name skryper --specpath . --clean skryper/main.py


REM Inform the user about the build location
echo.
echo Build complete! The executable can be found in the "dist" folder.
echo Press any key to deactivate the virtual environment and close this window...
pause > nul

REM Deactivate the virtual environment
deactivate

@echo off
cls

REM Running skryper.exe with logging (For development purposes)
echo Running skryper.exe with logging...
skryper.exe --logging

REM Pause to keep the window open until the user presses a key
echo.
echo Press any key to exit...
pause > nul

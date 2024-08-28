@echo off
cls

REM Running skryper.exe without logging (For development purposes)
echo Running skryper.exe without logging...
skryper.exe

REM Pause to keep the window open until the user presses a key
echo.
echo Press any key to exit...
pause > nul

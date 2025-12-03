@echo off
REM =========================================
REM Runner for python File Collector (Windows)
REM =========================================

cd /d "%~dp0..\logic"

python extract_codebase.py

echo.
echo ✅ Done! Press any key to close...
pause >nul

@echo off
setlocal enabledelayedexpansion

REM ===============================
REM This script formats and analyzes a Python file using Black, Pylint, Flake8, and mypy.
REM Please ensure that you have the following tools installed:
REM 
REM pip install black pylint flake8 mypy
REM 
REM To use this script, simply drag and drop a Python file onto it.
REM ===============================

REM Check if a file is passed as a parameter
if "%~1"=="" (
    echo Please drag and drop a Python file onto this batch script.
    pause
    exit /b
)

REM Name of the input file
set "INPUT_FILE=%~1"

REM Check if the input file exists
if not exist "%INPUT_FILE%" (
    echo The file %INPUT_FILE% does not exist.
    pause
    exit /b
)

REM Name of the output file based on the input file
set "OUTPUT_FILE=%~dpn1_code_report.txt"

REM Clear the output file if it exists
if exist "%OUTPUT_FILE%" del "%OUTPUT_FILE%"

echo Processing %INPUT_FILE%...

REM Add the raw code to the output file
echo -------------------------------------------------- >> "%OUTPUT_FILE%"
echo Source code of %INPUT_FILE%: >> "%OUTPUT_FILE%"
echo -------------------------------------------------- >> "%OUTPUT_FILE%"
type "%INPUT_FILE%" >> "%OUTPUT_FILE%"
echo -------------------------------------------------- >> "%OUTPUT_FILE%"

REM Format with Black
echo Formatting with Black... >> "%OUTPUT_FILE%"
black "%INPUT_FILE%" >> "%OUTPUT_FILE%" 2>&1

REM Check with Pylint
echo Checking with Pylint... >> "%OUTPUT_FILE%"
pylint "%INPUT_FILE%" >> "%OUTPUT_FILE%" 2>&1

REM Check with Flake8
echo Checking with Flake8... >> "%OUTPUT_FILE%"
flake8 "%INPUT_FILE%" >> "%OUTPUT_FILE%" 2>&1

REM Check with mypy
echo Checking with mypy... >> "%OUTPUT_FILE%"
mypy "%INPUT_FILE%" >> "%OUTPUT_FILE%" 2>&1

REM Add a separator
echo -------------------------------------------------- >> "%OUTPUT_FILE%"

REM Summary of results
echo Summary of results: >> "%OUTPUT_FILE%"
echo Black: >> "%OUTPUT_FILE%"
black --check "%INPUT_FILE%" >> "%OUTPUT_FILE%" 2>&1
echo -------------------------------------------------- >> "%OUTPUT_FILE%"
echo Pylint: >> "%OUTPUT_FILE%"
pylint "%INPUT_FILE%" --score=y --reports=n >> "%OUTPUT_FILE%" 2>&1
echo -------------------------------------------------- >> "%OUTPUT_FILE%"
echo Flake8: >> "%OUTPUT_FILE%"
flake8 "%INPUT_FILE%" >> "%OUTPUT_FILE%" 2>&1
echo -------------------------------------------------- >> "%OUTPUT_FILE%"
echo mypy: >> "%OUTPUT_FILE%"
mypy "%INPUT_FILE%" >> "%OUTPUT_FILE%" 2>&1
echo -------------------------------------------------- >> "%OUTPUT_FILE%"

echo Review completed. Results saved in %OUTPUT_FILE%.
pause

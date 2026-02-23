@echo off
chcp 65001 >nul 2>&1
title Post Analyzer - 5040
color 0A

echo ============================================
echo       Post Analyzer - Pro Runner
echo ============================================
echo.

REM --- Check Python ---
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python is not installed!
    echo         Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=2 delims= " %%V in ('python --version 2^>^&1') do (
    echo [OK] Python %%V
)

REM --- Setup venv ---
if not exist "venv" (
    echo [..] Creating virtual environment...
    python -m venv venv
    echo [OK] Virtual environment created.
)

call venv\Scripts\activate.bat

REM --- Install from requirements.txt ---
if exist "requirements.txt" (
    echo [..] Installing dependencies from requirements.txt...
    pip install --quiet --upgrade -r requirements.txt
    echo [OK] Dependencies installed.
) else (
    echo [WARN] requirements.txt not found, installing defaults...
    pip install --quiet --upgrade openpyxl pandas jdatetime
)

REM --- Check input file ---
if not exist "post.xlsx" (
    echo.
    echo [ERROR] Input file "post.xlsx" not found!
    echo         Place your data file in the same folder as this script.
    pause
    exit /b 1
)

echo.
echo ============================================
echo    Starting Analysis...
echo ============================================
echo.

python main.py

echo.
if %ERRORLEVEL% EQU 0 (
    echo ============================================
    echo    [OK] Analysis Complete!
    echo    Output: post_report.xlsx
    echo ============================================
) else (
    echo ============================================
    echo    [ERROR] Analysis failed!
    echo    Check the error messages above.
    echo ============================================
)

echo.
pause

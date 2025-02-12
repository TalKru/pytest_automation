@echo off
REM ===============================
REM run_all_tests.bat
REM ===============================

REM Activate the virtual environment
IF EXIST ".\.venv\Scripts\activate.bat" (
    call .\.venv\Scripts\activate.bat
) ELSE (
    echo Virtual environment not found. Please run windows_env_installer.bat first.
    pause
    exit /b 1
)

REM Run tests using pytest
pytest .\tests\

pause

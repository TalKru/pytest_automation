@echo off
REM ===============================
REM windows_env_installer.bat
REM ===============================
REM Optional: Instruct the user to update execution policy if not already done.
echo If you have not yet set your PowerShell execution policy to RemoteSigned, run:
echo    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
echo and choose [A] for "Yes to All".
pause

REM Check if the virtual environment exists; if not, create it.
REM NOTE! if PowerShell is used type: .\.venv\Scripts\Activate.ps1
IF NOT EXIST ".\.venv\Scripts\activate.bat" (
    echo Creating virtual environment...
    python -m venv .venv
)

REM Activate the virtual environment (using Command Prompt activation script).
call .\.venv\Scripts\activate.bat

REM Upgrade pip.
python -m pip install --upgrade pip

REM Install required packages.
python -m pip install -r requirements.txt

echo Requirements installed successfully.
pause

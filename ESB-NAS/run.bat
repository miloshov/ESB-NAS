@echo off
REM ESB-NAS Launcher Script
REM This script ensures the application runs correctly on Windows

echo ==============================================
echo  ESB-NAS - Emergency Notification Alert System
echo ==============================================
echo.

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed!
    echo.
    echo Please install Python 3.10 or higher:
    echo 1. Download from https://python.org
    echo 2. Run the installer
    echo 3. IMPORTANT: Check "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

echo [OK] Python found
python --version
echo.

REM Check if dependencies are installed
pip show flask >nul 2>&1
if errorlevel 1 (
    echo [INSTALL] Installing required packages...
    pip install flask flask-sqlalchemy flask-login waitress slack-sdk
    echo.
)

echo [START] Starting ESB-NAS...
echo.
echo Access at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

REM Run the application
python run.py

echo.
pause

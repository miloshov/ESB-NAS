@echo off
REM ESB-NAS Standalone Build Script for Windows
REM Run this script to create a standalone .exe application

echo ==============================================
echo  ESB-NAS Standalone Builder
echo ==============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python 3.10+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

echo [OK] Python found
echo.

REM Install PyInstaller if not present
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo [INSTALL] Installing PyInstaller...
    pip install pyinstaller
    echo.
) else (
    echo [OK] PyInstaller already installed
    echo.
)

REM Build the executable
echo [BUILD] Creating standalone executable...
echo This may take a few minutes...
echo.

pyinstaller --clean esb-nas.spec

if exist "dist\ESB-NAS.exe" (
    echo.
    echo ==============================================
    echo [SUCCESS] Standalone executable created!
    echo ==============================================
    echo.
    echo Location: %cd%\dist\ESB-NAS.exe
    echo.
    echo To run the application:
    echo   dist\ESB-NAS.exe
    echo.
    echo Default login:
    echo   Username: admin
    echo   Password: admin123
    echo.
    echo Access via browser: http://localhost:5000
    echo.
) else (
    echo [ERROR] Build failed! Check errors above.
)

pause

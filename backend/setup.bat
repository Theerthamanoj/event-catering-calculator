@echo off
REM Setup script for Event Catering Calculator Backend

echo.
echo ========================================
echo Event Catering Calculator - Backend Setup
echo ========================================
echo.

REM Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    exit /b 1
)

echo Detected Python:
python --version
echo.

REM Install dependencies
echo Installing dependencies...
python -m pip install -q -r requirements.txt
if %ERRORLEVEL% equ 0 (
    echo ✓ Dependencies installed
) else (
    echo ERROR: Failed to install dependencies
    exit /b 1
)
echo.

REM Seed database
echo Seeding database with sample data...
python seed.py
if %ERRORLEVEL% equ 0 (
    echo ✓ Database seeded
) else (
    echo ERROR: Failed to seed database
    exit /b 1
)
echo.

echo ========================================
echo ✓ Setup complete!
echo ========================================
echo.
echo To start the server, run:
echo   python app.py
echo.
echo Server will run on: http://localhost:5000
echo.

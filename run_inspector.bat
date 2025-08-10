@echo off
REM PowerPoint Inspector - Windows Batch File
REM This file makes it easy to run the PowerPoint Inspector tool on Windows

echo.
echo ========================================
echo    PowerPoint Inspector Tool
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    echo.
    pause
    exit /b 1
)

REM Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo No virtual environment found. Creating one...
    python -m venv venv
    call venv\Scripts\activate.bat
    
    echo Installing dependencies...
    pip install -r requirements.txt
)

REM Check if .env file exists
if not exist ".env" (
    echo.
    echo WARNING: .env file not found!
    echo Please create a .env file with your GEMINI_API_KEY
    echo You can copy .env.example and fill in your API key
    echo.
    echo Example .env file content:
    echo GEMINI_API_KEY=your_api_key_here
    echo.
)

echo.
echo Running PowerPoint Inspector...
echo.

REM Run the tool
python ppt_inspector.py %*

echo.
echo Tool execution completed.
echo.
pause

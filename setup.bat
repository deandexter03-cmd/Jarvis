@echo off
title JARVIS Setup
color 0A

echo ================================================
echo     J.A.R.V.I.S - Setup Wizard
echo ================================================
echo.
echo This will install everything you need to run JARVIS.
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed!
    echo.
    echo Please install Python 3.10 or higher from:
    echo https://python.org/downloads/
    echo.
    echo IMPORTANT: Check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo [OK] Python found!

REM Check if pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Pip not found. Try reinstalling Python.
    pause
    exit /b 1
)

echo [OK] Pip found!
echo.
echo Installing Python packages...
echo (This may take 1-2 minutes)
echo.

REM Install requirements
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to install packages.
    echo Try running as Administrator or manually run:
    echo pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo.
echo ================================================
echo     Setup Complete!
echo ================================================
echo.
echo Next steps:
echo 1. Install Ollama from https://ollama.com/download
echo 2. Open Command Prompt and run: ollama pull qwen3:1.7b
echo 3. Double-click run.bat to start JARVIS
echo.
echo The AI model download takes 2-3 minutes (about 1GB)
echo.
pause

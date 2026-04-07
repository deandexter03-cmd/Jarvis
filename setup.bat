@echo off
title J.A.R.V.I.S - Setup Wizard
color 0A

echo ================================================
echo    J.A.R.V.I.S - Enhanced AI Assistant Setup
echo ================================================
echo.
echo This will install all dependencies for Jarvis
echo.

:: Check if Python is installed
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed!
    echo.
    echo Please download and install Python 3.10+ from:
    echo https://www.python.org/downloads/
    echo.
    echo IMPORTANT: Check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)
echo [OK] Python found!
echo.

:: Check if Ollama is installed
echo [2/5] Checking Ollama installation...
ollama --version >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Ollama is not installed!
    echo.
    echo Please download and install Ollama from:
    echo https://ollama.com/download
    echo.
    echo After installing, come back and run this setup again.
    echo.
    pause
    exit /b 1
)
echo [OK] Ollama found!
echo.

:: Pull the AI model
echo [3/5] Downloading AI model (this may take a few minutes)...
ollama pull qwen3:1.7b
echo [OK] Model ready!
echo.

:: Install Python packages
echo [4/5] Installing Python dependencies...
pip install speechrecognition edge-tts pygame pyautogui pygetwindow psutil requests flask flask-cors beautifulsoup4 lxml
echo [OK] Dependencies installed!
echo.

:: Create necessary folders
echo [5/5] Creating folders...
if not exist "jarvis_docs" mkdir jarvis_docs
echo [OK] Folders ready!
echo.

:: Done!
echo ================================================
echo    SETUP COMPLETE!
echo ================================================
echo.
echo To start JARVIS:
echo   1. Make sure Ollama is running (ollama serve)
echo   2. Double-click jarvis.py or run: python jarvis.py
echo   3. Open browser to http://localhost:5050
echo.
echo The HUD will open automatically!
echo.
pause
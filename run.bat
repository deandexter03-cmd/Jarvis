@echo off
title J.A.R.V.I.S
color 0B

echo ================================================
echo     Starting J.A.R.V.I.S...
echo ================================================
echo.

REM Check if Ollama is running
curl -s http://localhost:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Ollama is not running!
    echo.
    echo Please start Ollama first:
    echo 1. Find Ollama in your system tray
    echo 2. Or open Command Prompt and run: ollama serve
    echo.
    echo Press any key to continue anyway...
    pause >nul
)

echo [OK] Starting JARVIS...
echo.
echo The HUD will open in your browser automatically.
echo Close this window to stop JARVIS.
echo.

python jarvis.py

echo.
echo JARVIS has stopped.
pause
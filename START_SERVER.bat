@echo off
REM Bitcoin Astrology - Live Server Launcher for Windows
REM Double-click this file to start the server!

echo ======================================================================
echo      BITCOIN FINANCIAL ASTROLOGY - LIVE SERVER
echo ======================================================================
echo.
echo Starting Python web server...
echo.

REM Change to the script directory
cd /d "%~dp0"

REM Start the server
python server.py

REM Keep window open if there's an error
pause

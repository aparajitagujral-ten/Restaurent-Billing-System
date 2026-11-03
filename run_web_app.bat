@echo off
title Restaurant Billing System (PS 43) - Web POS Server
echo ======================================================
echo    Starting Restaurant Billing Web Server (PS 43)
echo ======================================================
echo.
echo Launching local server and opening web browser...
echo.
python app.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Failed to start Python server.
    echo Please make sure Python 3 is installed and added to PATH.
    pause
)

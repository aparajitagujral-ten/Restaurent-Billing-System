@echo off
title Restaurant Billing System (PS 43) - Desktop GUI
echo Starting Restaurant Billing Desktop Application (Tkinter)...
python gui_app.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] An error occurred while launching GUI app.
    pause
)

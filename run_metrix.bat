@echo off
title VAVE Matrix Control Server
echo =========================================
echo   Starting VAVE Matrix Control System
echo =========================================
cd /d "c:\project\metrix"
echo.
echo Opening browser...
start http://localhost:5000
echo.
echo Running server... (Do not close this window)
python app.py
pause

@echo off
title BlackClipping - 100% Viral AI Clipper
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\start-windows.ps1"
echo.
echo   BlackClipping has stopped. Press any key to close this window.
pause >nul

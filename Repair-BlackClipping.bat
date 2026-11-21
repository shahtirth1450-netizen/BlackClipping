@echo off
title BlackClipping - Environment Repair Tool
cd /d "%~dp0"
echo ============================================================
echo   BlackClipping Self-Healing / Repair Tool
echo   Cleaning broken cache and resetting Python environment...
echo ============================================================
echo.
if exist ".venv" (
    echo [1/2] Removing damaged .venv folder...
    rmdir /s /q ".venv"
)
echo [2/2] Rebuilding fresh virtual environment and packages...
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\start-windows.ps1"
echo.
echo   Repair complete. Press any key to close this window.
pause >nul

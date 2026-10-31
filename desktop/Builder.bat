@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if not errorlevel 1 (
    py -3 compiler.py
) else (
    python compiler.py
)
if errorlevel 1 (
    echo Install Python 3.11 or newer with Tcl/Tk support and Node.js 22 or newer.
    pause
)

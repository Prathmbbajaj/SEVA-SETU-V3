@echo off
title Seva Setu - Frontend Web Application (Port 3000)
echo ==============================================================
echo   Seva Setu (सेवा सेतु) - Ministry of Cooperation
echo   Starting Frontend Web Server on http://localhost:3000
echo ==============================================================
echo.

cd /d "%~dp0"

rem Check if port 3000 is already held by a lingering process and free it
netstat -ano | findstr :3000 | findstr LISTENING >nul 2>&1
if %errorlevel% equ 0 (
    echo [Info] Port 3000 is already in use. Cleaning up lingering process...
    for /f "tokens=5" %%a in ('netstat -aon ^| findstr :3000 ^| findstr LISTENING') do taskkill /f /pid %%a >nul 2>&1
    timeout /t 1 /nobreak >nul
)

echo Opening browser at http://localhost:3000 ...
start http://localhost:3000

if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" -m http.server 3000 --directory frontend
) else (
    python -m http.server 3000 --directory frontend
)

pause

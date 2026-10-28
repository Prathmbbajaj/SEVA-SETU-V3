@echo off
title Seva Setu - FastAPI Backend (Port 8000)
echo ==============================================================
echo   Seva Setu (सेवा सेतु) - Ministry of Cooperation
echo   Starting Live FastAPI Backend on http://localhost:8000
echo   Swagger API Docs: http://localhost:8000/docs
echo ==============================================================
echo.

cd /d "%~dp0"

rem Check if port 8000 is already held by a lingering process and free it
netstat -ano | findstr :8000 | findstr LISTENING >nul 2>&1
if %errorlevel% equ 0 (
    echo [Info] Port 8000 is already in use. Cleaning up lingering process...
    for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000 ^| findstr LISTENING') do taskkill /f /pid %%a >nul 2>&1
    timeout /t 1 /nobreak >nul
)

if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" -m uvicorn main:app --app-dir backend --reload --port 8000
) else if exist "backend\venv\Scripts\python.exe" (
    "backend\venv\Scripts\python.exe" -m uvicorn main:app --app-dir backend --reload --port 8000
) else (
    python -m uvicorn main:app --app-dir backend --reload --port 8000
)

pause

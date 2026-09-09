@echo off
REM Startet iSlave per Doppelklick, ohne dass ein Terminal geoeffnet
REM werden muss. Sucht zuerst die virtuelle Umgebung .venv, danach die
REM normale Python-Installation.
chcp 65001 >nul
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8

if exist ".venv\Scripts\python.exe" (
    set "PY=.venv\Scripts\python.exe"
) else (
    where py >nul 2>nul && (set "PY=py -3") || (set "PY=python")
)

echo Starte iSlave...
echo.
%PY% src\main.py %*

echo.
echo iSlave wurde beendet.
pause

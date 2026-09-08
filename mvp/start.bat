@echo off
setlocal
cd /d "%~dp0.."
if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" -m mvp
    goto :done
)
where py >nul 2>nul
if not errorlevel 1 (
    py -3 -m mvp
    goto :done
)
where python >nul 2>nul
if not errorlevel 1 (
    python -m mvp
    goto :done
)
echo Python fehlt. Bitte Python 3.10 oder neuer inklusive Tcl/Tk installieren.
pause
exit /b 1
:done
if errorlevel 1 (
    echo Start fehlgeschlagen. Bitte die Fehlermeldung oben pruefen.
    pause
)

@echo off
setlocal
set "NIMO_RUNTIME=%LOCALAPPDATA%\NIMO"
if not exist "%NIMO_RUNTIME%" mkdir "%NIMO_RUNTIME%"
set "NIMO_ROOT=%NIMO_RUNTIME%"
set "NIMO_DB_PATH=%NIMO_RUNTIME%\nimo_memory.db"
set "NIMO_EXPORT_DIR=%NIMO_RUNTIME%\exports"
set "NIMO_LOG_PATH=%NIMO_RUNTIME%\nimo_error.log"
set "NIMO_VAULT_PATH=%NIMO_RUNTIME%\vault"
if exist "C:\Nimo\nimo_env\Scripts\python.exe" (set "NIMO_PYTHON=C:\Nimo\nimo_env\Scripts\python.exe") else (set "NIMO_PYTHON=python")
"%NIMO_PYTHON%" -B "%~dp0NIMO_TERMINAL_MASTER_4_0.py" --doctor
set "NIMO_EXIT=%ERRORLEVEL%"
echo.
if not "%NIMO_EXIT%"=="0" echo Doctor reported an actionable setup item. Review the JSON above.
endlocal & exit /b %NIMO_EXIT%

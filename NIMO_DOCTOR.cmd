@echo off
setlocal
if not defined LOCALAPPDATA (
  echo LOCALAPPDATA is unavailable. Run this check from a normal Windows user session.
  exit /b 2
)
set "NIMO_RUNTIME=%LOCALAPPDATA%\NIMO"
set "NIMO_VENV=%NIMO_RUNTIME%\venv"
set "NIMO_PYTHON=%NIMO_VENV%\Scripts\python.exe"
if not exist "%NIMO_PYTHON%" (
  echo NIMO is not installed for this Windows user. Run INSTALL_NIMO.cmd first.
  exit /b 2
)
set "NIMO_ROOT=%NIMO_RUNTIME%"
set "NIMO_DB_PATH=%NIMO_RUNTIME%\nimo_memory.db"
set "NIMO_EXPORT_DIR=%NIMO_RUNTIME%\exports"
set "NIMO_LOG_PATH=%NIMO_RUNTIME%\nimo_error.log"
set "NIMO_VAULT_PATH=%NIMO_RUNTIME%\vault"
"%NIMO_PYTHON%" -B "%~dp0NIMO_TERMINAL_MASTER_4_0.py" --doctor
set "NIMO_EXIT=%ERRORLEVEL%"
echo.
if not "%NIMO_EXIT%"=="0" echo Doctor reported an actionable setup item. Review the JSON above.
endlocal & exit /b %NIMO_EXIT%

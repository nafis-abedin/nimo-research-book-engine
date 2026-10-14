@echo off
setlocal
set "NIMO_RUNTIME=%LOCALAPPDATA%\NIMO"
if not exist "%NIMO_RUNTIME%" mkdir "%NIMO_RUNTIME%"
set "NIMO_ROOT=%NIMO_RUNTIME%"
set "NIMO_VENDOR=%~dp0vendor\pdf"
if exist "%NIMO_VENDOR%" set "PYTHONPATH=%NIMO_VENDOR%;%PYTHONPATH%"
set "NIMO_DB_PATH=%NIMO_RUNTIME%\nimo_memory.db"
set "NIMO_EXPORT_DIR=%NIMO_RUNTIME%\exports"
set "NIMO_LOG_PATH=%NIMO_RUNTIME%\nimo_error.log"
set "NIMO_VAULT_PATH=%NIMO_RUNTIME%\vault"
set "NIMO_PYTHON="
if /I "%~1"=="V4" shift
if exist "C:\Nimo\nimo_env\Scripts\python.exe" set "NIMO_PYTHON=C:\Nimo\nimo_env\Scripts\python.exe"
if not defined NIMO_PYTHON if exist "C:\Python314\python.exe" set "NIMO_PYTHON=C:\Python314\python.exe"
if not defined NIMO_PYTHON set "NIMO_PYTHON=python"
"%NIMO_PYTHON%" -B "%~dp0NIMO_TERMINAL_MASTER_4_0.py" %*
set "NIMO_EXIT=%ERRORLEVEL%"
endlocal & exit /b %NIMO_EXIT%

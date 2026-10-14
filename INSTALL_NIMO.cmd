@echo off
setlocal EnableExtensions
set "NIMO_RUNTIME=%LOCALAPPDATA%\NIMO"
set "NIMO_VENV=%NIMO_RUNTIME%\venv"
set "NIMO_PYTHON="
if exist "C:\Nimo\nimo_env\Scripts\python.exe" set "NIMO_PYTHON=C:\Nimo\nimo_env\Scripts\python.exe"
if not defined NIMO_PYTHON if exist "C:\Python314\python.exe" set "NIMO_PYTHON=C:\Python314\python.exe"
if not defined NIMO_PYTHON set "NIMO_PYTHON=py -3"
if /I "%~1"=="--help" goto help
if /I "%~1"=="/help" goto help
if not exist "%NIMO_RUNTIME%" mkdir "%NIMO_RUNTIME%"
where python >nul 2>&1
if errorlevel 1 if not exist "C:\Python314\python.exe" (
  echo Python 3 is required. Install it from https://www.python.org/downloads/windows/
  exit /b 2
)
echo [1/4] Creating isolated Python environment...
if not exist "%NIMO_VENV%\Scripts\python.exe" %NIMO_PYTHON% -m venv "%NIMO_VENV%"
if errorlevel 1 exit /b 3
echo [2/4] Installing core dependencies...
"%NIMO_VENV%\Scripts\python.exe" -m pip install --upgrade pip
"%NIMO_VENV%\Scripts\python.exe" -m pip install -r "%~dp0requirements.txt"
if errorlevel 1 exit /b 4
if /I "%~1"=="--optional" (
  echo [3/4] Installing optional research and media dependencies...
  "%NIMO_VENV%\Scripts\python.exe" -m pip install -r "%~dp0requirements-optional.txt"
  if errorlevel 1 exit /b 5
) else (
  echo [3/4] Optional dependencies skipped. Use INSTALL_NIMO.cmd --optional when needed.
)
echo [4/4] Running first health check...
set "NIMO_ROOT=%NIMO_RUNTIME%"
set "NIMO_DB_PATH=%NIMO_RUNTIME%\nimo_memory.db"
set "NIMO_EXPORT_DIR=%NIMO_RUNTIME%\exports"
set "NIMO_LOG_PATH=%NIMO_RUNTIME%\nimo_error.log"
set "NIMO_VAULT_PATH=%NIMO_RUNTIME%\vault"
"%NIMO_VENV%\Scripts\python.exe" -B "%~dp0NIMO_TERMINAL_MASTER_4_0.py" --doctor
set "NIMO_EXIT=%ERRORLEVEL%"
echo.
echo Installation complete. Use START_NIMO_FINAL.cmd to launch NIMO.
endlocal & exit /b %NIMO_EXIT%
:help
echo Usage: INSTALL_NIMO.cmd [--optional]
echo   no option  Install core NIMO dependencies only.
echo   --optional Install optional research, PDF, media and plotting dependencies.
exit /b 0

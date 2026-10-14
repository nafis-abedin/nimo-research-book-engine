@echo off
setlocal EnableExtensions
set "NIMO_RUNTIME=%LOCALAPPDATA%\NIMO"
set "NIMO_VENV=%NIMO_RUNTIME%\venv"
set "NIMO_BOOTSTRAP="
if /I "%~1"=="--help" goto help
if /I "%~1"=="/help" goto help
if not "%~2"=="" goto invalid_args
if not "%~1"=="" if /I not "%~1"=="--optional" goto invalid_args
if not defined LOCALAPPDATA (
  echo LOCALAPPDATA is unavailable. Run this installer from a normal Windows user session.
  exit /b 2
)
where py >nul 2>&1
if not errorlevel 1 set "NIMO_BOOTSTRAP=py -3"
if not defined NIMO_BOOTSTRAP (
  where python >nul 2>&1
  if not errorlevel 1 set "NIMO_BOOTSTRAP=python"
)
if not defined NIMO_BOOTSTRAP (
  echo Python 3.11 or newer is required. Install it from https://www.python.org/downloads/windows/
  exit /b 2
)
%NIMO_BOOTSTRAP% -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 11) else 1)"
if errorlevel 1 (
  echo Python 3.11 or newer is required. Update Python, then run this installer again.
  exit /b 2
)
if not exist "%NIMO_RUNTIME%" mkdir "%NIMO_RUNTIME%"
if errorlevel 1 exit /b 3
echo [1/5] Creating isolated Python environment...
if not exist "%NIMO_VENV%\Scripts\python.exe" %NIMO_BOOTSTRAP% -m venv "%NIMO_VENV%"
if errorlevel 1 exit /b 3
"%NIMO_VENV%\Scripts\python.exe" -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 11) else 1)"
if errorlevel 1 (
  echo The existing NIMO virtual environment uses Python older than 3.11.
  echo Remove only "%NIMO_VENV%" and rerun this installer to rebuild it.
  exit /b 3
)
echo [2/5] Installing required dependencies...
"%NIMO_VENV%\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 exit /b 4
"%NIMO_VENV%\Scripts\python.exe" -m pip install -r "%~dp0requirements.txt"
if errorlevel 1 exit /b 4
if /I "%~1"=="--optional" (
  echo [3/5] Installing optional research and media dependencies...
  "%NIMO_VENV%\Scripts\python.exe" -m pip install -r "%~dp0requirements-optional.txt"
  if errorlevel 1 exit /b 5
) else (
  echo [3/5] Optional PDF, media, plotting, and voice dependencies skipped.
  echo Use INSTALL_NIMO.cmd --optional only when you need those features.
)
echo [4/5] Registering the nimo command for this Windows user...
"%NIMO_VENV%\Scripts\python.exe" -B "%~dp0NIMO_WINDOWS_INSTALL.py" "%~dp0NIMO_TERMINAL_MASTER_4_0.py"
if errorlevel 1 (
  echo NIMO dependencies are installed, but command registration failed.
  echo You can still launch NIMO with START_NIMO_FINAL.cmd from this repository folder.
  exit /b 6
)
echo [5/5] Running first health check...
set "NIMO_ROOT=%NIMO_RUNTIME%"
set "NIMO_DB_PATH=%NIMO_RUNTIME%\nimo_memory.db"
set "NIMO_EXPORT_DIR=%NIMO_RUNTIME%\exports"
set "NIMO_LOG_PATH=%NIMO_RUNTIME%\nimo_error.log"
set "NIMO_VAULT_PATH=%NIMO_RUNTIME%\vault"
"%NIMO_VENV%\Scripts\python.exe" -B "%~dp0NIMO_TERMINAL_MASTER_4_0.py" --doctor
set "NIMO_EXIT=%ERRORLEVEL%"
echo.
if not "%NIMO_EXIT%"=="0" echo Doctor reported an actionable setup item. Review the JSON above.
if "%NIMO_EXIT%"=="0" (
  echo Installation complete. Close and reopen Command Prompt, then type: nimo
  echo Keep Ollama running in another window. If needed, start NIMO_OLLAMA_SERVER.cmd first.
)
endlocal & exit /b %NIMO_EXIT%
:help
echo Usage: INSTALL_NIMO.cmd [--optional]
echo   no option  Install core chat, online search, and page extraction dependencies.
echo   --optional Install PDF, media, voice, and plotting dependencies.
exit /b 0
:invalid_args
echo Unsupported installer argument. Use INSTALL_NIMO.cmd --help.
exit /b 2

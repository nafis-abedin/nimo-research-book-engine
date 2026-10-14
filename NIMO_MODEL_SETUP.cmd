@echo off
setlocal
set "NIMO_RUNTIME=%LOCALAPPDATA%\NIMO"
set "NIMO_VENV=%NIMO_RUNTIME%\venv"
if exist "%NIMO_VENV%\Scripts\python.exe" (set "NIMO_PYTHON=%NIMO_VENV%\Scripts\python.exe") else (set "NIMO_PYTHON=python")
echo ==== Ollama status ====
where ollama >nul 2>&1
if errorlevel 1 (
  echo Ollama is not installed or not on PATH.
  echo Install from https://ollama.com/download/windows
  exit /b 2
)
ollama --version
echo.
echo ==== Installed models ====
ollama list
echo.
echo NIMO detects installed Ollama models automatically.
echo No particular model is required by the public release.
echo For better book research, install a capable chat model in Ollama, for example:
echo   ollama pull qwen2.5:7b
echo Then launch NIMO and use /model to select or use auto mode.
endlocal


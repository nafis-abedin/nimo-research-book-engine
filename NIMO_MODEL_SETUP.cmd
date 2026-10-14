@echo off
setlocal
where ollama >nul 2>&1
if errorlevel 1 (
  echo Ollama is not installed or not on PATH.
  echo Install from https://ollama.com/download/windows
  exit /b 2
)
echo ==== Ollama status ====
ollama --version
if errorlevel 1 exit /b 3
echo.
echo ==== Installed models ====
ollama list
if errorlevel 1 (
  echo Ollama is installed, but its local service is not responding.
  echo Run NIMO_OLLAMA_SERVER.cmd in this window, leave it open, then use another Command Prompt for nimo.
  exit /b 3
)
echo.
echo NIMO discovers chat-capable models served by this Ollama installation.
echo If no model is listed, install one with: ollama run ^<model-name^>
echo Inside NIMO, use /model to list models or /model ^<exact-model-name^> to select one.
echo The model name must be available to Ollama; NIMO does not load other runtimes directly.
endlocal

@echo off
setlocal
where ollama >nul 2>&1
if errorlevel 1 (
  echo Ollama is not installed or not on PATH.
  echo Install Ollama from https://ollama.com/download/windows, then reopen Command Prompt.
  exit /b 2
)
ollama list >nul 2>&1
if not errorlevel 1 (
  echo Ollama is already responding. Do not start a second server.
  echo Open another Command Prompt and type: nimo
  exit /b 0
)
echo Starting the local Ollama service in this window.
echo Keep this window open, then open another Command Prompt and type: nimo
echo Press Ctrl+C here only when you want to stop the local model service.
echo.
ollama serve
set "NIMO_EXIT=%ERRORLEVEL%"
endlocal & exit /b %NIMO_EXIT%

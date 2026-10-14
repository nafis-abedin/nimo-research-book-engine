"""Register the installed NIMO runtime as a user-level Windows command."""

from __future__ import annotations

import ctypes
import ntpath
import os
import shutil
import sys
import tempfile
from pathlib import Path


def merge_user_path(existing: str, entry: str) -> tuple[str, bool]:
    """Append one Windows PATH entry once, preserving every existing entry."""
    target = ntpath.normcase(ntpath.normpath(entry.strip().strip('"')))
    entries = [part for part in str(existing or "").split(";") if part.strip()]
    if any(ntpath.normcase(ntpath.normpath(part.strip().strip('"'))) == target for part in entries):
        return str(existing or ""), False
    return ";".join([*entries, entry]), True


def launcher_text() -> str:
    """Return the PATH launcher; all user data paths resolve at runtime."""
    return """@echo off
setlocal
if not defined LOCALAPPDATA (
  echo LOCALAPPDATA is unavailable. Run NIMO from a normal Windows user session.
  exit /b 2
)
set "NIMO_RUNTIME=%LOCALAPPDATA%\\NIMO"
set "NIMO_APP=%NIMO_RUNTIME%\\app\\NIMO_TERMINAL_MASTER_4_0.py"
set "NIMO_PYTHON=%NIMO_RUNTIME%\\venv\\Scripts\\python.exe"
if not exist "%NIMO_APP%" (
  echo NIMO runtime is missing. Run INSTALL_NIMO.cmd again from the repository folder.
  exit /b 2
)
if not exist "%NIMO_PYTHON%" (
  echo NIMO Python environment is missing. Run INSTALL_NIMO.cmd again from the repository folder.
  exit /b 2
)
set "NIMO_ROOT=%NIMO_RUNTIME%"
set "NIMO_DB_PATH=%NIMO_RUNTIME%\\nimo_memory.db"
set "NIMO_EXPORT_DIR=%NIMO_RUNTIME%\\exports"
set "NIMO_LOG_PATH=%NIMO_RUNTIME%\\nimo_error.log"
set "NIMO_VAULT_PATH=%NIMO_RUNTIME%\\vault"
"%NIMO_PYTHON%" -B "%NIMO_APP%" %*
set "NIMO_EXIT=%ERRORLEVEL%"
endlocal & exit /b %NIMO_EXIT%
"""


def _broadcast_environment_change() -> None:
    """Notify Windows shells that the current user's PATH changed."""
    try:
        result = ctypes.c_size_t()
        ctypes.windll.user32.SendMessageTimeoutW(
            0xFFFF, 0x001A, 0, "Environment", 0x0002, 5000, ctypes.byref(result)
        )
    except (AttributeError, OSError):
        pass


def register_command(source_file: Path | None = None) -> dict[str, str | bool]:
    """Install a current runtime copy and register ``nimo`` in the user PATH."""
    if os.name != "nt":
        raise OSError("The NIMO command installer requires Windows")
    local_app_data = os.environ.get("LOCALAPPDATA", "").strip()
    if not local_app_data:
        raise OSError("LOCALAPPDATA is unavailable")

    source = (source_file or Path(__file__).with_name("NIMO_TERMINAL_MASTER_4_0.py")).resolve()
    if not source.is_file():
        raise FileNotFoundError("NIMO_TERMINAL_MASTER_4_0.py was not found beside the installer")
    runtime = Path(local_app_data) / "NIMO"
    app_dir, bin_dir = runtime / "app", runtime / "bin"
    app_dir.mkdir(parents=True, exist_ok=True)
    bin_dir.mkdir(parents=True, exist_ok=True)

    installed_app = app_dir / source.name
    with tempfile.NamedTemporaryFile(dir=app_dir, suffix=".tmp", delete=False) as handle:
        temporary = Path(handle.name)
    try:
        shutil.copyfile(source, temporary)
        temporary.replace(installed_app)
    finally:
        temporary.unlink(missing_ok=True)

    launcher = bin_dir / "nimo.cmd"
    launcher.write_text(launcher_text(), encoding="ascii", newline="\r\n")
    path_entry = r"%LOCALAPPDATA%\NIMO\bin"
    import winreg

    key = winreg.CreateKeyEx(
        winreg.HKEY_CURRENT_USER,
        "Environment",
        0,
        winreg.KEY_QUERY_VALUE | winreg.KEY_SET_VALUE,
    )
    try:
        try:
            current_path, _ = winreg.QueryValueEx(key, "Path")
        except FileNotFoundError:
            current_path = ""
        updated_path, changed = merge_user_path(str(current_path or ""), path_entry)
        if len(updated_path) > 32760:
            raise OSError("The current user PATH is too long to append the NIMO command safely")
        if changed:
            winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, updated_path)
    finally:
        winreg.CloseKey(key)
    if changed:
        _broadcast_environment_change()
    return {"runtime_app": str(installed_app), "command": str(launcher), "path_updated": changed}


def main() -> int:
    try:
        source = Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else None
        result = register_command(source)
    except Exception as exc:
        print(f"NIMO command registration failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1
    print(f"Installed NIMO runtime: {result['runtime_app']}")
    print(f"Registered CMD command: {result['command']}")
    if result["path_updated"]:
        print("The current user's PATH was updated. Close and reopen Command Prompt before typing nimo.")
    else:
        print("The NIMO command is already in the current user's PATH. Open a new Command Prompt if needed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

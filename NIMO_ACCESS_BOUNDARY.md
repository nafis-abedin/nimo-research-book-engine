# NIMO — Access Boundary

The public release only needs the files in this repository. Runtime state is stored outside the repository under `%LOCALAPPDATA%\\NIMO` by the supplied launchers.

NIMO communicates with Ollama through the local service at `http://127.0.0.1:11434`. Ollama manages its own model storage; NIMO does not require access to an Ollama model directory.

Do not add personal vaults, memory databases, logs, exports, jobs, backups, API keys, SSH keys, or machine-specific configuration to the repository.

Use `NIMO_DOCTOR.cmd` to inspect the current machine setup. Use `NIMO_MODEL_SETUP.cmd` to inspect installed Ollama models.

# Project Nimo — Access Boundary

The public release only needs the files in this repository. Runtime state and the optional DPAPI-protected secret store default outside the repository under `%LOCALAPPDATA%\\NIMO` on Windows, including when the Python file is launched directly. The launchers use the installed virtual environment and stop with an installation message if it is missing.

NIMO communicates with Ollama through the local service at `http://127.0.0.1:11434`. Ollama manages its own model storage; NIMO does not require access to an Ollama model directory.

Ordinary chat sends prompts to the local Ollama service. A clear request for research or current information can share its search query with the configured public search provider and fetch selected pages. `/offline` blocks web access. Do not include private details, credentials, or confidential case material in an online search request.

SQLite data, vault content, and ordinary database snapshots are not application-encrypted. Snapshots do not include vaults and are not encrypted. Store them on a protected drive.

By default, `%LOCALAPPDATA%\\NIMO` holds `nimo_memory.db`, the `vault\\` and `vault\\Research\\` folders, research outputs in `research\\`, job artifacts in `jobs\\`, exports, logs, and local configuration. Conversation memory persists across launches. NIMO retrieves relevant non-sensitive local records; `/clear` changes the active chat context but does not delete saved memory. Excluded, sensitive, expired, and deleted records are not supplied as conversation memory, and derived checkpoints are invalidated when one of their source records is removed or restricted.

Do not add personal vaults, memory databases, logs, exports, jobs, backups, API keys, SSH keys, or machine-specific configuration to the repository.

Use `NIMO_DOCTOR.cmd` to inspect the current machine setup. Use `NIMO_MODEL_SETUP.cmd` to inspect installed Ollama models.

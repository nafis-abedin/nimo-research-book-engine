# NIMO Research Book Engine — Runtime Notes

NIMO 4.0 is a local-first research and book-writing assistant. Launch it with `START_NIMO_FINAL.cmd` or `nimo.cmd`.

## Runtime data

The launchers store memory, jobs, exports, logs, vault links, and configuration under `%LOCALAPPDATA%\\NIMO`, outside the repository. This prevents personal runtime data from entering GitHub.

## Ollama

NIMO connects to the local Ollama service at `http://127.0.0.1:11434`. It discovers the models installed for the current user and does not assume the author's model. Use `/model` inside NIMO or `NIMO_MODEL_SETUP.cmd` to inspect model availability.

## Research and books

Use `/research deep <topic>` for evidence-oriented research and `/book <topic>` for book workflows. Review the source ledger, claim ledger, evidence gaps, dates, and limitations before publication. Internet retrieval is opt-in.

## Access

Keep personal vaults, databases, logs, backups, exports, and model files outside the repository. Never publish `%LOCALAPPDATA%\\NIMO`.

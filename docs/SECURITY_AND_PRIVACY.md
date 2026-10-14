# Security and Privacy Model

## Repository boundary

Only files in the release allowlist belong in the public repository. Local memory, vaults, exports, jobs, logs, backups, encryption material, model files, and machine configuration stay outside the repository.

## Local-first behavior

Ollama traffic defaults to loopback. Internet retrieval is opt-in. Retrieved content is treated as untrusted reference data and is not allowed to override runtime instructions.

## User responsibility

NIMO is a research assistant, not a publisher of record. Review sources, licenses, privacy implications, and high-consequence claims before distribution. Keep Windows, Python, Ollama, and dependencies updated.

## Limitations

SQLite and vault data are not application-level encrypted by default. Use a protected Windows account and BitLocker/device encryption. Do not place API keys or private credentials in prompts, notes, logs, or repository files.

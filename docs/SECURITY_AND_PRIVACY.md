# Project Nimo Security and Privacy Model

## Repository boundary

Only files in the release allowlist belong in the public repository. Local memory, vaults, exports, jobs, logs, backups, encryption material, model files, and machine configuration stay outside the repository.

## Local-first behavior

Ollama traffic defaults to loopback. Ordinary conversation remains local; a clear request for public research or current facts can enable web retrieval. `/offline` blocks retrieval until `/online` is used. Retrieved content is treated as untrusted reference data and is not allowed to override runtime instructions.

The prompt and attached text are sent to the user's local Ollama service. For an explicit research request, the search query is sent to DuckDuckGo or to Brave Search when configured; NIMO then fetches selected public pages. Search queries can reveal their subject and any text included in them to the provider. Keep credentials, private URLs, customer data, and confidential material out of online queries. Local model use does not mean that the selected search provider sees no query data when retrieval is requested.

By default, the local runtime root is `%LOCALAPPDATA%\\NIMO` on Windows, outside the source checkout. It contains `nimo_memory.db` (conversation and memory records), `vault\\` (including research evidence notes), `research\\` (research project outputs), `jobs\\` (background artifacts), `exports\\`, logs, and local configuration. Direct Python execution uses the same root. `NIMO_ROOT` and the documented `NIMO_*` path variables can override defaults. NIMO does not provide automatic cloud backup.

Conversation history remains in the local SQLite database until the user deletes it or purges expired records. NIMO creates deterministic, source-linked checkpoints after three exchanges and can retrieve relevant non-sensitive local records in later sessions. Excluded, sensitive, and expired messages are filtered from prompt context and semantic retrieval; when a message is excluded, deleted, marked sensitive, or expires, any checkpoint derived from it is invalidated. Use `/memory list`, `/memory search <text>`, `/memory-exclude <id>`, and `/memory delete <id> confirm` to manage memory. The database and vault are not application-encrypted, so use Windows account protection and device encryption.

The repository does not include an analytics SDK or automatic telemetry uploader. Files named `research_telemetry.json` or `job_telemetry.json` are local provenance and timing records written beside job artifacts; they are not sent to an analytics service. Other external requests are feature-driven: explicit web research uses a search provider and fetches selected public pages, while weather, RSS, and image lookup use their documented public services when those features are requested.

## User responsibility

NIMO is a research assistant, not a publisher of record. Review sources, licenses, privacy implications, and high-consequence claims before distribution. Keep Windows, Python, Ollama, and dependencies updated.

## Limitations

SQLite databases, vault notes, logs, exports, jobs, and ordinary snapshots are not application-level encrypted by default. Windows DPAPI protects the optional secret store for the current Windows user; this does not encrypt the other files. Use a protected Windows account and BitLocker/device encryption. Do not place API keys or private credentials in prompts, notes, logs, or repository files.

Online page fetching rejects local/private IP destinations, credentials in URLs, nonstandard ports, unsafe redirects, unsupported content types, and responses over its configured size limit. This lowers SSRF and resource-exhaustion risk; it is not a substitute for a hardened network sandbox or a guarantee against DNS rebinding or compromised public services.

The PDF reader opens the file with the operating system's default local PDF viewer. It does not start a local HTTP server or load a remote PDF.js script.

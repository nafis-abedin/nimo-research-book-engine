# NIMO Research Book Engine

NIMO is a **local-first, Ollama-powered research and book-writing engine** for evidence-oriented research, source-grounded drafting, and publisher review. It is designed to help a user move from a research question to a traceable manuscript without bundling the author's private data or a fixed AI model.

## Core purpose

- Conduct structured research with explicit evidence, dates, domains, limitations, and source ledgers.
- Keep retrieved evidence separate from model-generated synthesis.
- Support long-form book workflows with scope, chapter checkpoints, claim review, and export stages.
- Work with the Ollama models installed on the current computer; no model is bundled or assumed.
- Keep memory, databases, vault links, jobs, exports, logs, and configuration outside GitHub under `%LOCALAPPDATA%\\NIMO`.
- Provide a safe Windows installer, launchers, health checks, model discovery, and a reproducible SHA-256 release manifest.

## Main capabilities

- Local Ollama chat and runtime model discovery.
- Offline-first operation with explicit `/online` and `/offline` modes.
- Deep research workflow with source ledger, claim ledger, evidence gaps, retrieval timestamps, and limitations.
- Book workflow using `/book <topic>` after research scope review.
- Chapter checkpoints and publisher-oriented factual, citation, copyright, privacy, and defamation review prompts.
- Optional PDF, media, plotting, and richer research dependencies.
- Access boundary that keeps private runtime state out of the repository.

## Quick start on Windows

1. Install [Python](https://www.python.org/downloads/windows/) 3.11 or newer.
2. Install [Ollama](https://ollama.com/download/windows).
3. Clone or download this repository.
4. Run `INSTALL_NIMO.cmd` from the repository folder.
5. Run `NIMO_MODEL_SETUP.cmd` to inspect the Ollama models installed on that computer.
6. Run `NIMO_DOCTOR.cmd` and fix any reported required check.
7. Launch with `START_NIMO_FINAL.cmd` or `nimo.cmd`.

Core installation does not download an AI model. The user chooses and installs Ollama models separately. NIMO discovers available models at runtime and does not require the original author's model names.

For PDF, media, plotting, and optional research features, run:

```bat
INSTALL_NIMO.cmd --optional
```

## Research and book workflow

```text
/research deep <topic>
/research status
/book <topic>
/online
/offline
/model
```

Use `/research deep <topic>` first. Review the source ledger, claims, dates, domains, evidence gaps, and uncertainty. Only then start `/book <topic>`. Review every chapter checkpoint before export. A final manuscript still requires human fact-checking and editorial review.

## Privacy and security boundary

The repository intentionally excludes private databases, vaults, logs, jobs, exports, backups, encryption keys, local configuration, model files, generated manuscripts, personal documents, and machine-specific artifacts. Do not publish `%LOCALAPPDATA%\\NIMO` or copy its contents into GitHub.

Internet retrieval is opt-in. External lab commands are disabled by default and require an explicit allowlist and approval. NIMO does not automatically publish books, submit forms, or post to external services.

## Documentation

- [Detailed User Guide](docs/USER_GUIDE.md)
- [Book and Research Workflow](docs/BOOK_RESEARCH_WORKFLOW.md)
- [Security and Privacy](docs/SECURITY_AND_PRIVACY.md)
- [Access Boundary](NIMO_ACCESS_BOUNDARY.md)
- [Runtime Notes](NIMO_FINAL_README.md)

## Release status

This repository is a **private staging release candidate**. The clean package has passed fresh-clone checkout, Python AST validation, NIMO Doctor validation, forbidden-artifact scanning, and SHA-256 manifest generation. Public release should happen only after a fresh-machine installation test with a clean Windows user profile and a selected Ollama model.

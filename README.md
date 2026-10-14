# Project Nimo

Project Nimo is a **local-first, Ollama-powered research and writing assistant** for evidence-oriented research, source-grounded drafting, and manuscript review. Its Windows command and launcher filenames retain the `NIMO` prefix for compatibility. It helps users move from a research question to a traceable manuscript without bundling private data or a fixed AI model.

## Core purpose

- Conduct structured research with explicit evidence, dates, domains, limitations, and source ledgers.
- Keep retrieved evidence separate from model-generated synthesis.
- Support long-form book workflows with scope, chapter checkpoints, claim review, and export stages.
- Work with the Ollama models installed on the current computer; no model is bundled or assumed.
- Keep memory, databases, vault links, jobs, exports, logs, and configuration outside GitHub under `%LOCALAPPDATA%\NIMO`.
- Provide a safe Windows installer, launchers, health checks, model discovery, and a reproducible SHA-256 release manifest.

## Project note

Project Nimo is my first public software project. I am continuing to improve it, and I apologize for any rough edges or bugs. Clear, constructive issue reports are welcome and help guide future improvements.

## Main capabilities

- Local Ollama chat and runtime model discovery.
- Local-first conversation with automatic web retrieval for explicit research requests and an `/offline` network override.
- Deep research workflow with source ledger, claim ledger, evidence gaps, retrieval timestamps, and limitations.
- Book workflow using `/book <topic>` after research scope review.
- Chapter checkpoints and publisher-oriented factual, citation, copyright, privacy, and defamation review prompts.
- Optional PDF, media, plotting, and richer research dependencies.
- Access boundary that keeps private runtime state out of the repository.

## Quick start on Windows

1. Install [Python](https://www.python.org/downloads/windows/) 3.11 or newer.
2. Install [Ollama](https://ollama.com/download/windows).
3. Clone the public repository or download its ZIP archive, then open Command Prompt in the extracted folder.

```bat
git clone https://github.com/nafis-abedin/project-nimo.git
cd project-nimo
```

If Git is not installed, use GitHub's **Code → Download ZIP**, extract it, and open Command Prompt in that folder.

4. Start Ollama in a separate Command Prompt. From the repository folder, run `NIMO_OLLAMA_SERVER.cmd` and leave that window open. If Ollama is already running, the script detects it and does not start a duplicate service.
5. Open another Command Prompt in the repository folder and run `INSTALL_NIMO.cmd`.
6. Run `NIMO_MODEL_SETUP.cmd` and `NIMO_DOCTOR.cmd` to inspect installed models and the health check.
7. Close and reopen Command Prompt so Windows reloads the user PATH, then type `nimo` from any directory.

The installer creates a private environment and a current application copy under `%LOCALAPPDATA%\NIMO`, then registers a user-level `nimo` command. Re-run the installer after updating the repository to refresh that copy. It does not download an AI model. Install any chat-capable model through Ollama, then use `/model` or `/model <exact-installed-model-name>` to select it; manual selection is saved in the private local config. NIMO discovers model IDs at runtime; models installed in other runtimes are not loaded directly unless those runtimes expose an Ollama-compatible service.

If Ollama has no model yet, install one in another Command Prompt with `ollama run <model-name>` (Ollama may download it first), then use `/model` inside NIMO. The app uses the smallest installed chat-capable model in AUTO mode; `/model <name>` pins an exact installed model.

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

An ordinary conversation stays local by default. A request that clearly needs fresh research or a book automatically enables web retrieval for that task; `/offline` blocks all web requests until `/online` is used. `/network auto` restores this behavior. Search uses broad public-web providers rather than a hard-coded set of research websites, but no search provider indexes every page on the Internet.

Use `/research deep <topic>` first. Review the source ledger, claims, dates, domains, evidence gaps, and uncertainty. Search snippets are discovery leads only; only extracted page text can support claims. Only then start `/book <topic>`. Review every chapter checkpoint before export. A final manuscript still requires human fact-checking and editorial review.

## Privacy and security boundary

The repository intentionally excludes private databases, vaults, logs, jobs, exports, backups, encryption keys, local configuration, model files, generated manuscripts, personal documents, and machine-specific artifacts. Runtime data and DPAPI-protected secrets default to `%LOCALAPPDATA%\NIMO`, outside the checkout. The memory database is `nimo_memory.db`; the default vault is `vault`, research project output is `research`, asynchronous job artifacts are in `jobs`, and exported files are in `exports`. These locations can be customized in the local configuration or with the documented `NIMO_*` environment variables. Do not publish the runtime directory or copy its contents into GitHub. Online search sends the search query to the configured search provider and requests selected public pages; do not include passwords, API keys, private URLs, or confidential text in a query. Chat/model prompts go to the local Ollama service at loopback.

Ordinary chat stays local. An explicit request for research or fresh public information can enable retrieval, while `/offline` blocks all network retrieval until `/online` is used. External lab commands are disabled by default and require an explicit allowlist and approval. NIMO does not automatically publish books, submit forms, or post to external services.

## Documentation

- [Detailed User Guide](docs/USER_GUIDE.md)
- [Book and Research Workflow](docs/BOOK_RESEARCH_WORKFLOW.md)
- [Security and Privacy](docs/SECURITY_AND_PRIVACY.md)
- [Access Boundary](NIMO_ACCESS_BOUNDARY.md)

## Release status

This repository is a **public release candidate**, not a certified production release. CI checks syntax, regression tests, release boundaries, secrets patterns, and the SHA-256 manifest on supported Python versions. The project has not been validated on every Windows profile, Ollama model, proxy, search-provider account, or network. Run `INSTALL_NIMO.cmd`, `NIMO_DOCTOR.cmd`, and a local chat/research smoke test on your own computer before relying on it for important work.

## Search provider and factuality policy

DuckDuckGo is the default no-key search provider. For users who have a Brave Search API key, set `NIMO_BRAVE_API_KEY` in the local environment; never put it in the repository or a committed config file. NIMO records the provider used for each search and falls back safely if Brave is unavailable. Searches are broad public-web queries; the engine does not crawl the entire Internet or guarantee that every relevant page is indexed.

Search results are leads, not facts. NIMO requires source extraction, dates, source tiers, entity matching, independent corroboration, conflict reporting, and visible abstention for unresolved current claims. Read [Research Reliability](docs/RESEARCH_RELIABILITY.md) before using NIMO for a book or current-affairs research.

See [ROADMAP](ROADMAP.md) for planned future development and maintenance gates.

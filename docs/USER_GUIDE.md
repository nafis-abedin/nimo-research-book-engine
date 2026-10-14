# NIMO User Guide

This guide explains how a new Windows user can install, configure, use, and troubleshoot NIMO without knowing the internal architecture.

## 1. What NIMO is

NIMO is a local-first research and book-writing assistant. It uses the Ollama service running on the user's computer. It is **model-agnostic**: the repository does not contain an AI model and does not assume that another user has the same model as the developer.

NIMO supports two complementary modes:

- **Offline/local mode:** use installed Ollama models and local runtime data.
- **Online research mode:** explicitly retrieve current web evidence, then preserve source URLs, retrieval time, claims, evidence gaps, and limitations for review.

NIMO is an assistant, not an automatic publisher. Human review remains required for factual accuracy, citations, copyright, privacy, and defamation risk.

## 2. Install on a new Windows computer

### Required software

1. Install Python 3.11 or newer from <https://www.python.org/downloads/windows/>.
2. Install Ollama from <https://ollama.com/download/windows>.
3. Start Ollama once so its local service is available.
4. Clone this private repository or download its ZIP archive.

### Install NIMO

Open Command Prompt in the repository folder and run:

```bat
INSTALL_NIMO.cmd
```

This creates an isolated environment under `%LOCALAPPDATA%\\NIMO\\venv`, installs core Python dependencies, keeps runtime state outside the repository, and runs an initial health check.

For optional PDF, media, plotting, and richer research features:

```bat
INSTALL_NIMO.cmd --optional
```

Optional dependencies are not required for the core terminal workflow.

### Check the installation

```bat
NIMO_DOCTOR.cmd
```

A healthy core installation should report `ok: true` for Ollama connectivity, database/FTS5, disk, configuration, and plugins. Embeddings and vault are optional and may legitimately report disabled or not installed.

## 3. Configure Ollama models

NIMO does not download or bundle the author's model. Each user selects models appropriate for their own RAM, GPU, language needs, and licensing requirements.

Run:

```bat
NIMO_MODEL_SETUP.cmd
```

Inside NIMO, use:

```text
/model
```

NIMO discovers models exposed by the local Ollama service at `http://127.0.0.1:11434`. The model name can be different on every computer. A larger model may improve synthesis quality but require more memory and time.

Semantic retrieval embeddings are optional. If a user installs an Ollama embedding model supported by the project and enables embeddings, NIMO can build vector indexes. The core application remains usable without embeddings.

## 4. Start and stop NIMO

Start:

```bat
START_NIMO_FINAL.cmd
```

or:

```bat
nimo.cmd
```

Stop the terminal normally with the documented exit command or close the terminal after the current operation completes. Runtime state is stored outside the repository.

## 5. Basic research workflow

1. Start in offline mode unless current sources are required.
2. Use `/research deep <topic>` with a precise question and scope.
3. Review the generated source ledger, URLs, retrieval dates, domains, claims, evidence gaps, and limitations.
4. Follow up on missing or conflicting evidence.
5. Use `/online` only when current web retrieval is needed.
6. Return to `/offline` when finished retrieving.
7. Save or export only reviewed research artifacts.

Example:

```text
/research deep the history and current policy of [topic], with primary sources and dates
```

Do not treat a search snippet or headline as sufficient evidence for an important claim. Verify the original source, date, scope, geography, definition, and uncertainty.

## 6. Book-writing workflow

Use the book workflow only after the research scope is clear:

```text
/book <topic>
```

Recommended sequence:

1. Define audience, purpose, geography, date range, and exclusions.
2. Run deep research.
3. Review the source and claim ledgers.
4. Identify evidence gaps and conflicting sources.
5. Draft one chapter or checkpoint at a time.
6. Check every material claim against its source.
7. Verify quotations against the original document.
8. Review citations, dates, names, numbers, and uncertainty.
9. Review copyright, privacy, and defamation risks.
10. Export only after human editorial approval.

AI-generated prose must be edited and fact-checked before publication. NIMO should report insufficient evidence rather than inventing a claim.

## 7. Network and privacy controls

- `/offline` prevents optional online retrieval.
- `/online` enables the configured research retrieval path when current sources are needed.
- Runtime databases, memory, vault links, jobs, logs, exports, and configuration are stored under `%LOCALAPPDATA%\\NIMO`.
- Never commit `%LOCALAPPDATA%\\NIMO`, `.env` files, API keys, SSH keys, databases, logs, or generated manuscripts.
- External command/lab execution is disabled by default and requires an explicit configured allowlist and approval.

## 8. Troubleshooting

### Ollama is not detected

- Start the Ollama application.
- Confirm that `ollama` is on PATH.
- Run `NIMO_MODEL_SETUP.cmd`.
- Run `NIMO_DOCTOR.cmd` again.

### No chat model is available

Install at least one chat-capable model in Ollama. The correct model depends on the user's hardware. NIMO cannot use a non-Ollama model directly.

### Embeddings report disabled or not installed

This is optional for the core workflow. Install a compatible Ollama embedding model only if semantic retrieval is needed, then rerun the model setup and doctor checks.

### Online research is unavailable

Confirm that online mode is explicitly enabled, the configured provider is reachable, and the topic is not blocked by a network policy. NIMO should preserve an evidence gap rather than silently fabricate a source.

### Installation fails

Run `NIMO_DOCTOR.cmd`, record the first failing check, and keep the full error text private. Do not upload runtime logs or local databases to GitHub.

## 9. Safe update and backup practice

Pull or download updates into a clean folder. Keep runtime state outside Git. Before a major update, export only the artifacts that are safe to retain and verify their integrity. GitHub is the source repository for sanitized code and documentation; it is not a substitute for a separate encrypted backup of private runtime data.

# Project Nimo User Guide

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
3. Clone the public repository or download its ZIP archive.

```bat
git clone https://github.com/nafis-abedin/project-nimo.git
cd project-nimo
```

Without Git, choose **Code → Download ZIP** on the repository page, extract it, and open Command Prompt in that folder.

### Start Ollama in its own Command Prompt

After cloning or extracting the project, run this from a separate Command Prompt in the repository folder:

```bat
NIMO_OLLAMA_SERVER.cmd
```

Leave this window open while using NIMO. If Ollama is already responding, the script reports that and avoids starting a second server. If Ollama has no model yet, run `ollama run <model-name>` in a Command Prompt; Ollama downloads the selected model if necessary.

### Install NIMO

Open Command Prompt in the repository folder and run:

```bat
INSTALL_NIMO.cmd
```

This creates an isolated environment under `%LOCALAPPDATA%\NIMO\venv`, installs core chat and online-research dependencies, keeps runtime state outside the repository, registers a user-level `nimo` command, copies the current runtime under `%LOCALAPPDATA%\NIMO\app`, and runs an initial health check. The launch and Doctor commands use this same environment. If it is missing, they stop and tell you to install NIMO instead of silently switching to another Python installation. Re-run the installer after updating the repository to refresh the installed runtime copy.

After installation, close and reopen Command Prompt so it reloads the PATH entry. You can then run `nimo` from any directory. Use a second terminal for NIMO; keep the Ollama server terminal open.

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

NIMO discovers chat-capable models exposed by the local Ollama service at `http://127.0.0.1:11434`. The model name can be different on every computer. AUTO chooses the smallest installed chat-capable model; pin a model by its exact installed name with `/model <model-name>`, and use `/model auto` to return to AUTO. Manual selection is saved in the private local config and restored when that model is available. Any model installed in Ollama can be selected, including models imported from elsewhere. Other runtimes are not loaded directly unless they provide an Ollama-compatible service. A larger model may improve synthesis quality but require more memory and time.

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

1. Ordinary chat uses local models by default. Ask directly for research or current sources when needed; NIMO switches online for that retrieval. `/offline` blocks online retrieval, `/online` explicitly enables it, and `/network auto` restores automatic behavior.
2. Use `/research deep <topic>` with a precise question and scope. NIMO uses the currently selected model; set a different one first with `/model`, or pass `--model <installed-model-name>` to `/research`.
3. Review the generated source ledger, URLs, retrieval dates, domains, claims, evidence gaps, and limitations.
4. Follow up on missing or conflicting evidence.
5. Recheck unresolved claims with a focused follow-up while online retrieval is allowed.
6. Use `/offline` when you want to block network retrieval.
7. Save or export only reviewed research artifacts.

Example:

```text
/research deep the history and current policy of [topic], with primary sources and dates
```

Do not treat a search snippet or headline as sufficient evidence for any factual claim. NIMO retains snippets only as discovery leads; claims must be grounded in extracted page text. Verify the original source, date, scope, geography, definition, and uncertainty. Public-web search providers do not index the entire Internet, so a search is broad but not exhaustive.

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

- `/offline` blocks online retrieval until `/online` is used.
- In AUTO mode, explicit fresh research/book requests enable retrieval for the task; ordinary local conversation does not automatically access the web.
- Online lookups send the search query to DuckDuckGo, or to Brave when you configure its API key, and fetch selected public pages. Do not search private notes, credentials, confidential case details, or private URLs unless you are comfortable sharing the query with that provider.
- Chat messages and attached local content are sent to the Ollama service on your own computer; NIMO does not send them to an OpenAI or NIMO cloud model.
- Runtime databases, memory, vault links, jobs, logs, exports, and configuration are stored under `%LOCALAPPDATA%\\NIMO`.
- Conversation messages are stored in the local `nimo_memory.db` database. NIMO builds a deterministic checkpoint after three complete exchanges and retrieves relevant non-sensitive memory across later sessions. The checkpoint preserves labeled source messages; it does not ask the small chat model to rewrite or guess what was said. `/clear` starts a fresh active context but leaves saved memory available for relevant recall.
- Use `/memory list`, `/memory search <text>`, `/memory-exclude <id>`, `/memory restore <id>`, and `/memory delete <id> confirm` to inspect and manage saved conversation records. Excluded, sensitive, and expired records are omitted from recent prompt context and retrieval; deleting a source invalidates summaries based on it. `/memory purge` removes expired records.
- By default, the local data root is `%LOCALAPPDATA%\\NIMO`: conversation database `nimo_memory.db`; vault and evidence notes `vault\\` (including `vault\\Research\\`); research project outputs `research\\`; background job artifacts `jobs\\`; exports `exports\\`; logs `nimo_error.log`; and local configuration `nimo_config.json`. `NIMO_ROOT`, `NIMO_DB_PATH`, `NIMO_VAULT_PATH`, `NIMO_EXPORT_DIR`, and `NIMO_LOG_PATH` can change these locations.
- The database and vault are not application-encrypted; use Windows account protection and device encryption.
- Never commit `%LOCALAPPDATA%\\NIMO`, `.env` files, API keys, SSH keys, databases, logs, or generated manuscripts.
- External command/lab execution is disabled by default and requires an explicit configured allowlist and approval.

## 8. Troubleshooting

### Ollama is not detected

- Run `NIMO_OLLAMA_SERVER.cmd` in a separate Command Prompt and leave it open, or start the Ollama application.
- Confirm that `ollama` is on PATH.
- Run `NIMO_MODEL_SETUP.cmd`.
- Run `NIMO_DOCTOR.cmd` again.

### No chat model is available

Install at least one chat-capable model in Ollama, then run `/model`. The correct model depends on the user's hardware. A model from another source can be used after it is available through Ollama; NIMO does not directly load model files or connect to unrelated runtime APIs.

### Embeddings report disabled or not installed

This is optional for the core workflow. Install a compatible Ollama embedding model only if semantic retrieval is needed, then rerun the model setup and doctor checks.

### Online research is unavailable

Confirm that online mode is explicitly enabled, the configured provider is reachable, and the topic is not blocked by a network policy. NIMO should preserve an evidence gap rather than silently fabricate a source.

### Installation fails

Run `NIMO_DOCTOR.cmd`, record the first failing check, and keep the full error text private. Do not upload runtime logs or local databases to GitHub.

## 9. Safe update and backup practice

Pull or download updates into a clean folder. Keep runtime state outside Git. Before a major update, export only the artifacts that are safe to retain and verify their integrity. GitHub is the source repository for sanitized code and documentation; it is not a substitute for a separate encrypted backup of private runtime data.

NIMO's `/backup snapshot` and `nimo --backup` create a local SQLite snapshot. They do not encrypt the snapshot or include your vault and job files. Store backups only on a protected drive and use BitLocker or another trusted encryption method for sensitive data.

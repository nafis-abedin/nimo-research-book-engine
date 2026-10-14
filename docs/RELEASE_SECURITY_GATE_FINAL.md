# NIMO 4.0 — Final Public Release Audit

Date: 2026-10-14

## Decision

`PUBLIC_PUBLISH = BLOCKED_PENDING_GITHUB_STAGING`

The release tree is clean and passes local static/runtime gates. Public GitHub publication remains a separate staging action that must be followed by a fresh clone test.

## Content audit

- Every release file was read or parsed.
- Python source: AST parse passed.
- Python source: compile passed with `python -B`.
- Python source contains 9,283 lines and 521 definitions.
- Sensitive external operations were reviewed: Ollama HTTP calls, public web retrieval, file writes, subprocess calls, SSH/lab execution, backup/restore, and optional media tools.
- Prompt-injection examples in the quality test fixture were replaced with neutral payload labels. Untrusted research text remains data and cannot override the system boundary.

## Security gates

- Ollama default is loopback-only: pass.
- Plaintext secret-file check: pass.
- DPAPI availability check on Windows: pass.
- Redaction probe: pass.
- External lab commands: disabled by default and allowlisted/approval-gated.
- Shell chaining and redirection: blocked for lab commands.
- Research retrieval: bounded, read-only, credential-free URL policy.
- Runtime state: outside the repository under `%LOCALAPPDATA%\\NIMO`.
- Personal Windows paths in public documentation: removed.
- Forbidden runtime artifacts in release tree: none.

## Runtime gates

- `nimo.cmd --version`: pass.
- `NIMO_DOCTOR.cmd`: pass on fresh runtime state; optional embedding model and unconfigured vault are reported as optional.
- SHA-256 release manifest: pass.
- Launcher uses `python -B`: pass.

## Known limitations

- At least one chat-capable Ollama model must be installed by the user.
- Embeddings are optional and require the configured embedding model.
- PDF/media features need optional dependencies.
- SQLite and vault data are not application-level encrypted; Windows account protection and BitLocker/device encryption are recommended.
- Human review remains required before publishing factual or copyrighted book content.

## Next release gate

Create a private GitHub staging repository, clone it into a new empty folder, run the installer and doctor, test one Ollama chat, test one research artifact, and only then consider public visibility.
# release-manifest.sha256 stores canonical content hashes.
# Text files are normalized from CRLF to LF before hashing so verification is
# identical on Windows and Linux; binary files are hashed byte-for-byte.

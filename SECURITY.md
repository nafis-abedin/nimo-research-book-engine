# Security Policy

NIMO is a local-first research and book-writing tool. Please do not publish credentials, private documents, local databases, model files, or personal research artifacts in issues or pull requests.

## Reporting a vulnerability

For a private repository, report a suspected vulnerability through GitHub's private repository communication or a private security advisory. Do not disclose an exploitable detail publicly before a fix is available.

Include the affected version or commit, operating system, reproduction steps, impact, and a minimal proof of concept. Redact tokens, personal data, and private URLs.

## Supported release line

The `v4.0.x` release line is the current release candidate line. Security fixes should be tested against the latest tagged release and `main`.

## Security boundaries

NIMO does not bundle an Ollama model, does not automatically publish research, does not submit forms, and keeps runtime state outside the repository under `%LOCALAPPDATA%\NIMO` on Windows.

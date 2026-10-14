# Project Nimo Security Policy

NIMO is a local-first research and book-writing tool. Please do not publish credentials, private documents, local databases, model files, or personal research artifacts in issues or pull requests.

## Reporting a vulnerability

Report suspected vulnerabilities through GitHub's **Report a vulnerability** flow or a private security advisory when that feature is enabled. If private reporting is unavailable, contact the repository owner privately. Do not post credentials, private data, or an exploitable proof of concept in a public issue.

Include the affected version or commit, operating system, reproduction steps, impact, and a minimal proof of concept. Redact tokens, personal data, and private URLs.

## Supported release line

The `v4.0.x` release line is the current release candidate line. Security fixes should be tested against the latest tagged release and `main`.

## Security boundaries

NIMO does not bundle an Ollama model, does not automatically publish research, does not submit forms, and keeps runtime state outside the repository under `%LOCALAPPDATA%\NIMO` on Windows.

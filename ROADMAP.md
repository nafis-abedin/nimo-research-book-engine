# Project Nimo Development Roadmap

NIMO is a public release candidate. A stable production release still depends on the research reliability, installation, and human-review gates below.

## Phase A — release safety

- Maintain a clean public boundary with no runtime state or historical source snapshots.
- Keep `SECURITY.md`, `CONTRIBUTING.md`, README, release notes, SHA-256 manifest, CI, dependency monitoring, and a protected `main` branch.
- Run fresh-clone installation tests on a clean Windows profile.

## Phase B — source-grounded factuality

- Store provider, retrieval time, publication time, update time, canonical URL, source tier, and content hash for every source.
- Require at least two independent publisher groups for current high-impact claims.
- Separate official/primary evidence, independent reporting, secondary summaries, and lead-only sources.
- Detect conflicting values and show the conflict instead of selecting a convenient answer.
- Refuse a current answer when the source date or entity identity cannot be verified.
- Add a human-reviewed evaluation set for office holders, elections, prices, laws, releases, health, finance, and breaking news.

## Phase C — search quality

- Keep DuckDuckGo as the no-key fallback.
- Support opt-in Brave Search through `NIMO_BRAVE_API_KEY`; never commit the key.
- Add freshness filters, country/language targeting, user-configurable source preferences (without hard-coded discovery exclusions), pagination limits, and retry/backoff.
- Prefer direct pages over snippets and require page extraction before a claim enters the evidence ledger.
- Add retrieval metrics such as top-k relevance, source diversity, freshness compliance, citation coverage, groundedness, and answer completeness.

## Phase D — book-quality workflow

- Generate a perspective-diverse outline before drafting long chapters.
- Require every factual paragraph to map to evidence or be explicitly labeled interpretation, synthesis, or uncertainty.
- Run contradiction, date, citation, copyright, privacy, defamation, and attribution review before export.
- Preserve chapter checkpoints and allow the author to reject or revise unsupported passages.

## Phase E — release

- Complete the evaluation set with a high pass rate and inspect every failure.
- Complete clean-machine installation and offline/online smoke tests.
- Publish a prerelease first, then a stable release only after human review.

## Phase B implementation status
- Implemented strict current/high-impact claim gates requiring primary/official evidence and an independent publisher group.
- Added visible `CONTESTED` classification for correction, retraction, dispute, and contradiction signals.
- The regular online chat and `/web` paths now extract linked pages, preserve source tiers and dates, and ignore search snippets as evidence. Bengali current office-holder questions trigger date-aware official-plus-independent retrieval.
- Current claims require directly extracted, dated pages; maintained government directories may use their explicit update date for freshness.
- Bangladesh state news is grouped with government sources and cannot alone count as independent corroboration.
- Added regression tests in `tests/test_phase_b_factuality.py` and a human-review case set in `evaluation/phase_b_cases.jsonl`.
- CI now runs the Phase B factuality regression suite alongside compile, secret, boundary, and manifest checks.
- Human review of the evaluation set remains required before any public stable release.
- Core installation includes the search and page-extraction dependencies; launchers must use the installed virtual environment and fail visibly when it is missing.
- Repository defaults keep memory, logs, exports, configuration, and secret storage outside the checkout. Local model calls remain on loopback.
- Web page extraction rejects nonpublic destinations, unsafe redirects, non-text pages, and oversized responses; this is a risk reduction, not a guarantee against DNS rebinding or compromised public hosts.
- The PDF reader opens the OS default viewer to avoid an unauthenticated local file server and remote viewer script.
- `/backup` creates/verifies non-encrypted SQLite snapshots only. It does not encrypt, back up the vault, or upload data.
- A clean Windows profile install and Ollama smoke test still need to be completed before calling the release production-ready.

# NIMO Development Roadmap

NIMO remains private until the research reliability gates below are implemented and reviewed.

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
- Add freshness filters, country/language targeting, source-domain allowlists, pagination limits, and retry/backoff.
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

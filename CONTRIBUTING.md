# Contributing to NIMO

NIMO prioritizes evidence quality, reproducibility, privacy, and safe local operation.

## Before opening a change

1. Read `SECURITY.md`, `NIMO_ACCESS_BOUNDARY.md`, and `docs/RESEARCH_RELIABILITY.md`.
2. Keep secrets, model files, databases, logs, exports, and personal documents out of the repository.
3. Make changes small and explain the user-facing behavior and risk boundary.
4. Run `python -m py_compile NIMO_TERMINAL_MASTER_4_0.py` and `NIMO_DOCTOR.cmd` on Windows.
5. Update the SHA-256 release manifest when tracked files change.

## Research changes

Changes that affect retrieval, source selection, citations, dates, confidence, or book drafting must include a regression case showing what evidence is accepted, what evidence is rejected, and how uncertainty is displayed.

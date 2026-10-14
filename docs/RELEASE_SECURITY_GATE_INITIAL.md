# Release Security Gate — Initial Audit

Date: 2026-10-14

## Decision

PUBLIC_PUBLISH = BLOCKED

## Reason

The original working directory contains local runtime state, private memory, encryption material, backups, historical source snapshots, generated outputs, bundled dependencies, and unrelated application material. The public release is therefore staged in a separate allowlisted directory.

## Allowlist

- .gitignore
- README.md
- NIMO_FINAL_README.md
- NIMO_ACCESS_BOUNDARY.md
- NIMO_TERMINAL_MASTER_4_0.py
- nimo.cmd
- START_NIMO_FINAL.cmd
- docs/RELEASE_SECURITY_GATE_INITIAL.md
- release-manifest.sha256

## Exclusions

Databases, vaults, logs, jobs, exports, backups, keys, local configuration, temporary patches, generated artifacts, unrelated apps, node_modules, Python environments, vendor binaries, and personal files.

## Findings

- The original folder is not safe to publish as-is.
- Secret-pattern scanning produced many dependency-text false positives; those files are excluded from the release tree.
- A clean tree must be scanned again after installer/docs work is complete.
- No GitHub repository has been created yet.

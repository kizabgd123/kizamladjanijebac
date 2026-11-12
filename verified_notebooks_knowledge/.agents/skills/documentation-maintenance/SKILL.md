---
name: documentation-maintenance
description: Synchronize, update, and maintain project documentation, runbooks, and audit reports.
---

# Documentation Maintenance Skill

## When to Activate
Activate after completing implementation tasks, updating configurations, or concluding milestones.

## Required Context
- `README.md`, `docs/*.md`, and `BOOTSTRAP_REPORT.md`.
- Live system state, test outputs, and configuration files.

## Execution Steps
1. Review changes against existing documentation.
2. Update relevant architectural and operational documents in `docs/`.
3. Apply explicit status labels (`IMPLEMENTED`, `CONFIGURED`, `TESTED`, `PLANNED`, `BLOCKED`, `UNVERIFIED`).
4. Ensure code snippets and CLI commands in documentation match live system behavior.

## Verification & Checks
- All documented paths, commands, and options are validated.
- No aspirational claims are marked as IMPLEMENTED without verification.

---
name: system-diagnostics
description: Run comprehensive system, environment, runtime, and CLI diagnostics.
---

# System Diagnostics Skill

## When to Activate
Activate during baseline discovery, troubleshooting environment issues, or pre-flight verification.

## Required Context
- Host OS environment variables, PATH, and installed binaries (`agy`, `python3`, `uv`).

## Execution Steps
1. Execute `agy --version` and check `agy.version.json`.
2. Execute `python3 --version` and `uv --version`.
3. Check git status, current branch, and remote configuration.
4. Verify directory permissions and disk availability.
5. Record diagnostic findings into `docs/BOOTSTRAP_DISCOVERY.md`.

## Verification & Checks
- All required command lines return 0 exit codes.
- Report any missing or incompatible tools immediately.

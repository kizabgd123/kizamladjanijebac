---
name: testing-validation
description: Execute deterministic test suites, regression benchmarks, and Antigravity customization validations.
---

# Testing & Validation Skill

## When to Activate
Activate before merging changes, after completing tasks, and during release qualification.

## Required Context
- Automated test suite in `tests/`.
- Antigravity customization validator `scripts/validate_antigravity.py`.

## Execution Steps
1. Run `python3 scripts/validate_antigravity.py` to ensure all agent, skill, rule, and hook manifests conform to schema.
2. Run `pytest tests/ -q` to execute unit and regression suites.
3. Check corpus integrity by verifying SHA-256 hashes against `data/corpus_baseline_hashes.sha256`.
4. Capture exit codes and execution summaries into test reports.

## Verification & Checks
- All tests pass with exit code 0.
- Report any regressions or failed assertions immediately.

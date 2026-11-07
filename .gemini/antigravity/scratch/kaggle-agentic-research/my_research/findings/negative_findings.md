# Negative Findings Graveyard (Mandatory Failure Ledger)

Every failed hypothesis, regression, bug, or computational dead end MUST be logged here to prevent recursive agent loops.

| Exp ID | Hypothesis Tested | Observed vs Expected | Root Cause Analysis | Invariant / Negative Rule | Date |
|---|---|---|---|---|---|
| EXP-001a | Direct execution via system python (`python3 -m pytest`) | FAILED (`ModuleNotFoundError: No module named 'vertexai'`) | System interpreter lacks GCP SDK dependencies (`google-cloud-aiplatform`, `google-adk`). | **RULE:** NEVER run bare `python` or `pytest`; always execute inside `.venv/bin/` or via `uv run`. | 2026-11-06 |
| EXP-002a | Naive `content.split('---')` frontmatter extraction | FAILED (`AttributeError: 'NoneType' object has no attribute 'keys'`) | Inner markdown comments containing `---` (e.g. `# --- Required ---`) break naive string splits. | **RULE:** NEVER use naive delimiter split; use strict line-by-line `line.strip() == "---"` parser as implemented in `_setup_utils.py`. | 2026-11-06 |
| EXP-003 | Full-tier coverage in current `EVAL.yaml` | 0 assertions for `rating`, `stock`, `manufacturer`, `variants` | Evaluation suite only asserts on `Basic` and `Standard` columns. | **RULE:** Do not claim evaluation validation for Extended/Full attributes without expanding `EVAL.yaml`. | 2026-11-06 |

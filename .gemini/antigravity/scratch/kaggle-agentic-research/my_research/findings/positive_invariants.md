# Positive Invariants Ledger

Documented architectural, algorithmic, and parameter configurations with verified empirical gains.

| ID | Discovery | Empirical Delta | Verification Ref | Date |
|---|---|---|---|---|
| INV-001 | Isolated `uv` / `.venv` environment execution | 100% test pass rate vs ModuleNotFoundError on bare python | `EXP-001b` / `task-83` | 2026-11-06 |
| INV-002 | `_setup_utils.py:load_config` line-delimited `---` parser | Preserves frontmatter without splitting on inner markdown comments | `EXP-002` / `load_config` | 2026-11-06 |
| INV-003 | Strict boolean flag decoupling (`surface_gemini_skill` vs `surface_agents_skill`) | Clean persona separation across Gemini CLI / Desktop and ADK / Claude / Antigravity | `Makefile` / `design-spec.md` | 2026-11-06 |
| INV-004 | Negative assertion anti-hallucination guard (`no_hallucination: [Bose, AirPods, Sennheiser]`) | Deterministic catch of LLM out-of-catalog brand fabrication | `EVAL.yaml` cases 1 & 4 | 2026-11-06 |

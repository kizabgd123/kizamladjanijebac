---
trigger: glob
globs:
  - "tests/**"
---

# Testing & Quality Gate Verification Rule

1. **Deterministic Offline Tests:** Test suites must execute locally without requiring network access or paid LLM tokens. Use mock fixtures and local test embeddings.
2. **Comprehensive Coverage:** Every core module (`agent_reuse`, `ars_gate`, `mcts`, `ast_sandbox`, `rag_pipeline`, `metrics`) must have dedicated unit test files.
3. **Quality Gate Verification:** Assert that composite RAG scores satisfy $Q_{rag} \ge 0.80$ and fail if Answer Faithfulness is violated.
4. **Pre-Commit Verification:** Run `python3 scripts/validate_antigravity.py` and `pytest tests/` before declaring milestones complete.

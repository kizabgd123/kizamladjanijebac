# Formal Research Hypotheses

**Protocol Version:** 1.0  
**Target:** `retail-product-search`  

---

### Hypothesis HYP-001: Runnability & Import Isolation Verification
- **Statement:** The core entrypoint `scripts.agent:root_agent` can be loaded and validated within a clean Python 3.11+ environment using `tests/test_runnability.py` without requiring active GCP network or credentials when imported.
- **Theoretical Justification:** Decoupling module-level import side-effects from runtime GCP connections guarantees that the agent can be evaluated in air-gapped CI/CD environments.
- **Intervention / Parameter Delta:** Run `pytest tests/test_runnability.py` using local Python runtime.
- **Falsification Boundary:** Assertion failure, uncaught exception, or timeout $> 10$s.
- **Expected Information Gain:** Establishes whether static agent import is leak-free and decoupled from active cloud infrastructure.

---

### Hypothesis HYP-002: YAML Frontmatter Mutation Integrity
- **Statement:** Parsing and mutating `assets/design-spec.md` preserving YAML frontmatter headers prevents `_setup_utils.py` crashes (`'NoneType' object has no attribute 'get'`).
- **Theoretical Justification:** `_setup_utils.py` relies on `yaml.safe_load` on the delimited header; pure markdown conversion strips the mapping object.
- **Intervention / Parameter Delta:** Validate YAML structure extraction on `assets/design-spec.md`.
- **Falsification Boundary:** Frontmatter is missing or fails `isinstance(data, dict)`.
- **Expected Information Gain:** Confirms root cause of setup crashing during automated agent scaffolding.

---

### Hypothesis HYP-003: EVAL.yaml Assertion Coverage Mapping
- **Statement:** The 10 test cases in `EVAL.yaml` provide 100% coverage across the 4 schema field tiers (`Basic`, `Standard`, `Extended`, `Full`) and cover all critical failure modes documented in `troubleshooting.md`.
- **Theoretical Justification:** Verifying evaluation schema completeness ensures that model hallucinations, currency issues, and missing categories are rigorously bounded before cloud deployment.
- **Intervention / Parameter Delta:** Map each assertion and rubric rule in `EVAL.yaml` to catalog fields and failure modes.
- **Falsification Boundary:** Any schema field tier or critical failure mode with 0 test assertions.
- **Expected Information Gain:** Quantifies gaps in the test harness before deploying to production.

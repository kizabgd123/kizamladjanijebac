# Experiment Execution Log

Log initialized at 2026-11-06T23:24:58Z.

---

### [EXP-001] Import Isolation & Runnability Test
- **Timestamp:** 2026-11-06T23:31:15Z / 2026-11-06T23:39:06Z
- **Command (Trial 1):** `pytest tests/test_runnability.py` (system Python 3.12.3)
  - **Result:** FAILED (Exit 1)
  - **Error:** `scripts/agent.py:29: ModuleNotFoundError: No module named 'vertexai'`
- **Command (Trial 2):** `uv run pytest tests/test_runnability.py` (isolated venv CPython 3.14.6)
  - **Result:** PASSED (Exit 0)
  - **Metric:** 1 passed in 9.22s resolution + runtime (100% test pass rate)
  - **Artifacts:** Virtual environment `.venv` populated with 83 packages including `google-adk`, `google-cloud-aiplatform`, `google-genai`.

---

### [EXP-002] YAML Frontmatter Parser & Mutation Safety
- **Timestamp:** 2026-11-06T23:41:39Z
- **Command:** `python3 -c "from scripts._setup_utils import load_config; cfg = load_config('assets/design-spec.md'); ..."`
- **Result:** PASSED (Exit 0)
- **Extracted Keys:** `['gcp_project_id', 'data_source', 'product_fields', 'gcp_region', 'dataset_id', 'table_id', 'catalog_size', 'surface_gemini_skill', 'surface_agents_skill']`
- **Verification Ref:** `scripts/_setup_utils.py:load_config()` safely parses frontmatter with line-delimited `---` matching and avoids inner markdown comments.

---

### [EXP-003] EVAL.yaml Schema & Assertion Coverage Audit
- **Timestamp:** 2026-11-06T23:42:00Z
- **Analysis:** 10 evaluation test cases evaluated against the 4 product field tiers (`Basic`, `Standard`, `Extended`, `Full`).
- **Result:**
  - `Basic` & `Standard` fields (`name`, `price`, `description`, `category`, `brand`) have 100% test coverage with deterministic assertions and anti-hallucination lists.
  - `Extended` fields (`rating`, `stock`, `manufacturer`) and `Full` fields (`variants`, `specifications`, `reviews`) have 0% assertion coverage in `EVAL.yaml`.

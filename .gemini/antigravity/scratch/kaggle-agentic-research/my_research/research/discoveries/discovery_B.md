# Discovery Report: Agent B (Personas, Q-MODE Scaffolding & Evaluation Suite)

**Agent ID:** Agent_B_Evaluation  
**Date:** 2026-11-06T23:29:30Z  
**Target:** `retail-product-search`  

## 1. Domain Background & Surfacing Taxonomy
The skill supports multi-persona deployment through explicit boolean toggles in `Makefile` (`SURFACE_GEMINI_SKILL`, `SURFACE_AGENTS_SKILL`):
- **Persona 1 (Desktop & CLI):** Deployed to `~/.gemini/skills/retail-product-search` and symlinked into `~/.gemini/config/skills/`.
- **Persona 2 (AI Coding Assistants):** Symlinked to `~/.agents/skills/retail-product-search` (supporting ADK, Claude Code, Antigravity).
- **Persona 3 (Direct Makefile CLI):** Manual provisioning via `make setup PROJECT_ID=...`.
- **Persona 4 (Managed Cloud Agent):** Cloud Run, Agent Garden, and Gemini Enterprise App deployment.

## 2. Mechanistic Insights & The Q-MODE Protocol
1. **Strict Conversational Interception (Q-MODE):**
   - If no catalog is loaded, the agent MUST immediately output the verbatim Q-MODE prompt:
     `[skill: retail-product-search] active.`
     `Q-MODE: Pick a setup mode? [default: 1]`
     `  1. Quick start -- 2 questions, smart defaults, ~60s.`
     `  2. Full setup  -- 4 questions, ~2 min.`
   - Premature planning, unsolicited explanations, or skipped interview questions violate the protocol contract.
2. **`design-spec.md` Mutation Invariant:**
   - `bootstrap.sh` copies a template with YAML frontmatter.
   - If an agent rewrites `design-spec.md` from scratch as pure Markdown, `setup.py` crashes with `'NoneType' object has no attribute 'get'` in `_setup_utils.py`. The agent must strictly mutate values in-place.
3. **Evaluation Framework (`EVAL.yaml`):**
   - 10 structured benchmark test cases:
     * `headphones_under_200`, `cheapest_item`, `keyboard_search`, `category_filter`, `brand_search`, `no_results_handling`, `comparison_query`, `price_range`, `vague_query_handling`, `skill_covers_vector_search`.
   - Dual validation:
     * **LLM-as-judge rubric:** Negative hallucination constraints (e.g. forbidding mention of Bose, AirPods when catalog only has generic items).
     * **Deterministic assertions:** `tool_called: retrieve_docs`, `contains_product`, `price_under`, `graceful_no_results`.

## 3. Initial Hypotheses
- **HYP-B1 (Semantic Leaking in Numerical Constraints):** Because `scripts/retrievers.py:search()` is pure semantic similarity, queries like "under $50" or "between $50 and $150" rely entirely on prompt-level LLM filtering. In catalogs with dense embeddings, precision drops on price constraints unless top_k is expanded.
- **HYP-B2 (ADK Session Poisoning):** When the retriever encounters a transient network error or unindexed collection, the LLM incorporates the failure in session history and permanently stops calling `retrieve_docs` in subsequent turns until the session is explicitly cleared.

## 4. Identified Risk Factors & Edge Cases
- **Currency Agnosticism:** USD is hardcoded in `sample-products.csv`. Asking in EUR causes the agent to treat currencies as 1:1 without exchange rate translation.
- **Vague Query Misattribution:** For "I need something for my desk", semantic search might match peripheral items unless the prompt enforces category boundary grounding.

## 5. Open Questions for Relay Phase
- How can the evaluation assertions in `EVAL.yaml` be executed locally without live GCP billing credentials?
- What is the exact contract between `test_runnability.py` and the full `EVAL.yaml` test suite?

# ADR-001: Selection of Dual-Speed Production Engine (Option C) & Framework Separation

- **Status:** APPROVED & ADOPTED
- **Date:** 2026-11-12
- **Deciders:** Lead AI Systems Architect, Antigravity Orchestration Engineer
- **Context:** HALO RAG STUDIO Bootstrap on `/home/kizamladjanijebac/verified_notebooks_knowledge`

---

## 1. Context and Problem Statement
The legacy RAG and multi-agent setup operated on rigid linear prompt chains (e.g. 4-step sequential Express pipelines), suffering from high latency on repeated queries, token budget ballooning, lack of verifiable quality metrics, and brittle action execution. 

We require an autonomous, modular, and verifiable RAG and multi-agent system built on the verified 15-document knowledge corpus, integrated with Google Antigravity IDE and `agy` CLI, without introducing redundant or circular frameworks.

---

## 2. Decision Drivers
1. **Extreme Resource Efficiency:** Reduce latency and token consumption on repetitive/familiar intents.
2. **Deterministic Quality & Verification:** Ensure responses are grounded in the verified corpus with measurable metrics (RAGAS).
3. **Safe Policy Execution:** Ensure any generated code execution passes static AST analysis and least-privilege policies.
4. **Clean Architectural Separation:** Distinctly separate developer coordination (Antigravity IDE) from application execution (HALO runtime).
5. **No Redundant Frameworks:** Avoid stacking LangGraph, CrewAI, AutoGen, and ADK simultaneously.

---

## 3. Considered Architectural Options

### Option A: Pragmatic Modular Evolution
- Incremental refactoring of linear steps into modular RAG.
- Simple LRU cache, basic ARS-Lite.
- *Verdict: Rejected.* Insufficient reasoning depth for complex, multi-hop queries.

### Option B: Full Autonomous HALO Engine & CaP / LMP
- Full MCTS tree search and dynamic role instantiation on every query.
- *Verdict: Rejected for pure production.* Prohibitively high token consumption and latency overhead on routine inquiries.

### Option C: Dual-Speed Production Engine (SELECTED 🏆)
- **Fast-Path (70-80% of traffic):** AgentReuse semantic intent caching + ARS (Adaptive Reasoning Suppression with 3 certainty checkpoints). Delivers sub-100ms response on cached plans, ~93% latency reduction, and up to 53% token savings.
- **Deep-Path (20-30% of traffic):** HALO 3-Tier Hierarchy (High-Level Planner -> Mid-Level Role Designer -> Low-Level MCTS) coupled with AST-validated Code as Policies (CaP).
- *Verdict: Adopted.* Combines blistering speed and resource economy for standard queries with bounded, rigorous reasoning for ambiguous, multi-hop problems.

---

## 4. Architectural Separation of Frameworks

```
+-------------------------------------------------------------------------+
|                       DEVELOPER ORCHESTRATION LAYER                     |
|                                                                         |
|   Google Antigravity IDE  <======>  Antigravity CLI (`agy` v1.5.6)     |
|   - Agent Manager / Subagents       - Skills (.agents/skills/)          |
|   - Custom Agents (.agents/agents/) - Rules (.agents/rules/)            |
|   - Lifecycle Hooks (hooks.json)    - Workspace Instructions (AGENTS.md)|
+------------------------------------+------------------------------------+
                                     | (builds, tests, validates)
                                     v
+-------------------------------------------------------------------------+
|                         HALO APPLICATION RUNTIME                        |
|                                                                         |
|   FAST-PATH                         DEEP-PATH                           |
|   - AgentReuse (LRU + SQLite)       - 3-Tier HALO Reasoning             |
|   - ARS (3 Checkpoints: tau1..3)    - MCTS (Depth 3, Sims 8, c=1.414)   |
|                                     - CaP with AST Policy Guard         |
|                                                                         |
|                         MODULAR RAG ENGINE                              |
|   - Query Rewriter -> Semantic Router -> Hybrid BM25/Vector Retriever   |
|   - Grounded Citation Engine -> RAGAS 4-Metric Quality Gate (0.80)     |
+------------------------------------+------------------------------------+
                                     | (model inference abstraction)
                                     v
+-------------------------------------------------------------------------+
|                        LITELLM PROVIDER ABSTRACTION                     |
|   - JSON-driven provider registry (`providers.json`)                   |
|   - Gemini 3.8 / Local vLLM / Ollama / OpenAI-compatible endpoints     |
+-------------------------------------------------------------------------+
```

### Framework Evaluation Summary:
- **Google Antigravity IDE & `agy` CLI:** Sole primary developer orchestration layer.
- **Google Antigravity SDK (`google-antigravity`):** Evaluated. Kept as an optional application adapter rather than core runtime to prevent circular dependencies.
- **Google Agent Development Kit (`google-adk`):** Evaluated. Not adopted in initial core; custom modular Python engine provides tighter AST sandboxing and deterministic testing without monolithic overhead.
- **LiteLLM:** Adopted as universal multi-model abstraction layer via JSON configuration.

---

## 5. Initial Configuration Preset (Balanced Production)
All runtime settings are declared in `config/halo.yaml`:
- ARS Checkpoints: $\tau_1 = 0.90$ (Intent), $\tau_2 = 0.85$ (Retrieval), $\tau_3 = 0.80$ (Faithfulness).
- MCTS Parameters: Rollout Depth = 3, Simulations = 8, $C_{puct} = 1.414$, Random Seed = 42.
- CaP Constraints: Timeout = 5000ms, Memory Boundary = 128MB, AST Forbidden: `Import`, `ImportFrom`, `exec`, `eval`, dunder attributes.
- RAG Weights: Context Relevance 0.25, Answer Faithfulness 0.35, Answer Relevance 0.25, Noise Robustness 0.15. Minimum Composite Quality Gate: 0.80.

---

## 6. Consequences & Invariants
- **Corpus Immutability:** Source Markdown documents `01_...` to `15_...` are read-only.
- **Safety Over Speed:** High-risk queries, external side-effects, or contradictory evidence automatically bypass Fast-Path into Deep-Path.
- **Offline Reproducibility:** Default test suites must run deterministically without paid API keys.

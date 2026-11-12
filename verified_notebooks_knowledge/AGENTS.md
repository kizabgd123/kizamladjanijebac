# HALO RAG STUDIO — PROJECT AGENT CONSTITUTION

**Project Root:** `/home/kizamladjanijebac/verified_notebooks_knowledge`  
**System Architecture:** Option C — Dual-Speed Production Engine (Fast-Path AgentReuse/ARS + Deep-Path HALO MCTS/CaP)  
**Parent Authority:** `~/.gemini/MASTER_ORCHESTRATION.md`  

---

## 🏛️ Immutable Project Laws

### Law 1: Evidence Before Claims
Never state that a test passed, a model responded, an agent executed, or an index was created without providing concrete terminal or file-based evidence. If something fails or is blocked, report the exact error.

### Law 2: Corpus Invariance & Non-Contamination
The 15 source documents in `/home/kizamladjanijebac/verified_notebooks_knowledge/` (`01_...` to `15_...`) are ground truth and read-only.
- Never edit, reformat, or rename any source document.
- Never ingest generated documentation, test logs, caches, or agent prompts back into the knowledge corpus.
- Baseline SHA-256 hashes in `data/corpus_baseline_hashes.sha256` must match at all times.

### Law 3: Separation of Concerns
- **Developer Layer:** Coordinated by native Google Antigravity IDE, `agy` CLI, `.agents/` customizations, and subagents.
- **Application Layer:** Executed by HALO core Python modules (`src/core/`, `src/rag/`, `src/providers/`).
- Never mix application runtime dependencies with IDE agent definitions.

### Law 4: Dual-Speed Routing Protocol
- **Fast-Path:** Queries with matched semantic intent ($\ge 0.92$) and ARS certainty $\ge 0.90$ reuse validated execution plans.
- **Deep-Path:** Novel, ambiguous, safety-critical, or low-certainty queries must undergo 3-tier HALO planning with bounded MCTS.
- High-risk operations or contradictory retrieved chunks must NEVER exit early on confidence alone.

### Law 5: Code as Policies (CaP) AST Boundary
Any model-generated policy or query code must pass strict AST validation prior to execution:
- Prohibited: `Import`, `ImportFrom`, `exec`, `eval`, dunder attributes (`__*__`), and arbitrary OS/subprocess calls.
- Static AST validation is a policy layer; true isolation requires process-level sandboxing.

### Law 6: Quality Gate Thresholds
- RAG Composite Quality Gate: $Q_{rag} \ge 0.80$ across Context Relevance (0.25), Answer Faithfulness (0.35), Answer Relevance (0.25), and Noise Robustness (0.15).
- A high overall average must never mask a failure in Answer Faithfulness or Citation Grounding.

### Law 7: Work Log Governance
Every agent modification must update `WORK_LOG.md` adhering to the JudgeGuard task-budget limit ($\le 5$ concurrent active tasks).

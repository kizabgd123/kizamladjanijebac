# HALO RAG STUDIO

**Autonomous Multi-Agent & Modular RAG Engine on Google Antigravity**

[![Status](https://img.shields.io/badge/Status-IMPLEMENTED-brightgreen.svg)]()
[![Architecture](https://img.shields.io/badge/Architecture-Option%20C%20Dual--Speed-blue.svg)]()
[![Platform](https://img.shields.io/badge/Orchestrator-Google%20Antigravity%20IDE-orange.svg)]()
[![Python](https://img.shields.io/badge/Python-3.12%2B-blue.svg)]()

---

## 1. Overview
**HALO RAG Studio** transforms static knowledge exploration into an autonomous, dual-speed multi-agent engineering platform. Operating directly within the **Google Antigravity IDE** and utilizing the Antigravity CLI (`agy`), HALO grounds reasoning in an immutable, verified 15-document research corpus.

---

## 2. Problem & Goals
Traditional RAG setups suffer from:
- **Brittle Sequential Prompting:** Linear chains lack backtracking, dynamic role formulation, and search tree optimization.
- **Resource Churn & Latency:** Repeating identical or semantically similar queries incurs expensive RAG operations on every call.
- **Overthinking & Reasoning Degeneration:** Simple lookups pay the full token cost regardless of certainty.
- **Unverified Assertions:** Answers lack verifiable citation trails and rigorous multi-dimensional evaluation metrics.

**HALO Solves This By:**
- Implementing **Option C: Dual-Speed Production Engine** (Fast-Path AgentReuse/ARS + Deep-Path HALO MCTS/CaP).
- Guaranteeing **0% source modification** and strict citation attribution to verified notebooks.
- Enforcing **AST-sandboxed Code as Policies (CaP)**.
- Achieving **~93% plan reuse** and **~99% latency reduction** on familiar query intents.

---

## 3. Option C: Dual-Speed Architecture

```
                                 [User Query]
                                      |
                       +--------------v--------------+
                       |   Execution Policy Engine   |
                       +--------------+--------------+
                                      |
                 +--------------------+--------------------+
                 |                                         |
     (Safe / Intent Match)                        (Novel / High Risk / Ambiguous)
                 v                                         v
   +---------------------------+             +---------------------------+
   |         FAST-PATH         |             |         DEEP-PATH         |
   | - AgentReuse Plan Cache   |             | - 3-Tier HALO Reasoning   |
   | - ARS Checkpoints 1 & 2   |             | - MCTS (Depth 3, Sims 8)  |
   | - Sub-10ms Plan Reuse     |             | - AST-Guarded CaP Python  |
   +-------------+-------------+             +-------------+-------------+
                 |                                         |
                 +--------------------+--------------------+
                                      |
                                      v
                       +-----------------------------+
                       |     MODULAR RAG ENGINE      |
                       | - Semantic Router           |
                       | - Hybrid BM25/Vector Search |
                       | - Grounded Citation Engine  |
                       | - RAGAS 4-Metric Evaluator  |
                       +-----------------------------+
```

---

## 4. Fast-Path Architecture
- **AgentReuse Engine (`src/core/agent_reuse.py`):** In-memory LRU + persistent SQLite plan cache. Operates at semantic similarity threshold $\sigma \ge 0.92$, achieving sub-10ms plan reuse.
- **Adaptive Reasoning Suppression (`src/core/ars_gate.py`):**
  - **Checkpoint 1 ($\tau_1 = 0.90$):** Surface/intent certainty for immediate exit on routine questions.
  - **Checkpoint 2 ($\tau_2 = 0.85$):** Retrieval relevance certainty enabling direct synthesis without deep search.
  - **Checkpoint 3 ($\tau_3 = 0.80$):** Synthesis faithfulness verification.
- **Safety Bypass:** Queries with destructive keywords (`rm`, `sudo`, `delete`, `drop`) or unverified corpus states immediately bypass Fast-Path into Deep-Path with human oversight.

---

## 5. Deep-Path Architecture
- **3-Tier HALO Paradigm:** High-Level Goal Decomposition $\to$ Mid-Level Role Designer $\to$ Low-Level MCTS Inference.
- **MCTS Reasoner (`src/core/mcts.py`):** Bounded rollout depth 3, simulation count 8, exploration factor $C_{puct} = 1.414$, deterministic random seed 42, and maximum execution budget 10,000 ms.
- **Code as Policies (`src/core/ast_sandbox.py`):** Generates executable Python policy logic strictly validated against forbidden AST nodes (`Import`, `ImportFrom`, `exec`, `eval`, dunder attributes).

---

## 6. Modular RAG Pipeline
The 5-stage pipeline (`src/rag/`) enforces complete provenance:
1. **Ingestion (`ingestion.py`):** Ingests all 15 source documents, verifying SHA-256 hashes against `data/corpus_baseline_hashes.sha256`.
2. **Chunking (`chunking.py`):** Header-aware hierarchical chunking retaining document ID, title, category, and section path.
3. **Semantic Router (`semantic_router.py`):** Maps queries to target notebook domains (Cognitive, Enterprise AI, Antigravity, Personal Strategy).
4. **Hybrid Retriever (`hybrid_retriever.py`):** Merges pure-Python BM25 sparse keyword scoring with dense cosine similarity.
5. **Citation Engine (`citation_engine.py`):** Injects verifiable citations (`[Source: {filename} § {heading} ({chunk_id})]`).
6. **Metrics Evaluator (`metrics.py`):** Evaluates Context Relevance ($w=0.25$), Answer Faithfulness ($w=0.35$), Answer Relevance ($w=0.25$), and Noise Robustness ($w=0.15$), enforcing the Composite Quality Gate ($Q_{rag} \ge 0.80$).

---

## 7. Google Antigravity Development Environment
Developer coordination runs natively in Google Antigravity:
- **CLI (`agy` v1.5.6):** Available at `~/.gemini/bin/agy`.
- **Project Customizations (`.agents/`):**
  - `agents/`: 12 specialized role manifests with YAML frontmatter.
  - `skills/`: 10 reusable domain skills.
  - `rules/`: 7 system rules with validated triggers (`always_on`, `model_decision`, `glob`).
  - `hooks.json`: Lifecycle hooks for `SessionStart` integrity checks and `PostToolUse` validation.
  - `mcp_config.json`: Project-scoped filesystem MCP configuration.
- **Workspace Conscience (`AGENTS.md`):** Immutable project instructions and evidence standards.

---

## 8. Agent Team & Roles
| Agent | Role | Scope | Permitted Tools |
|---|---|---|---|
| `orchestrator` | Master Coordinator | Dependency management, verification gatekeeper | Read/write, terminal |
| `planner` | Strategic Planner | Task breakdown, DAG generation, milestone tracking | Read-only |
| `researcher` | Technical Researcher | Codebase inspection, source document analysis | Read-only |
| `architect` | Systems Architect | Interface definitions, ADR maintenance | Read-only |
| `rag-engineer` | RAG Systems Engineer | Ingestion, chunking, retrieval, citations, metrics | Read/write, terminal |
| `agent-engineer` | Agent Runtime Engineer | AgentReuse, ARS, MCTS, AST sandbox | Read/write, terminal |
| `integration-engineer` | Integration Engineer | LiteLLM configurations, MCP connectivity | Read/write, terminal |
| `implementer` | Software Implementer | Production code implementation | Read/write, terminal |
| `qa-tester` | QA & Test Engineer | Automated tests, regression benchmarks | Read/write, terminal |
| `code-reviewer` | Code Reviewer | Static analysis, architecture compliance | Read-only |
| `security-auditor` | Security Auditor | AST boundary audits, secret leakage checks | Read-only |
| `documentation-agent` | Technical Writer | Documentation synchronization and reporting | Read-only |

---

## 9. Installation & Development Setup

### Prerequisites
- Linux / macOS
- Python 3.12+
- `uv` (recommended) or `python3-venv`
- Google Antigravity IDE (`agy` CLI)

### Quick Start
```bash
# Clone or navigate to the workspace
cd /home/kizamladjanijebac/verified_notebooks_knowledge

# Run automated setup script
./scripts/setup_dev.sh

# Activate virtual environment
source .venv/bin/activate
```

---

## 10. CLI & Verification Commands

```bash
# 1. Verify source corpus integrity
python3 scripts/verify_corpus_integrity.py

# 2. Validate Antigravity customization schemas
python3 scripts/validate_antigravity.py

# 3. Run automated test suite
pytest tests/ -v

# 4. Antigravity CLI model inspection
~/.gemini/bin/agy models
```

---

## 11. Security & Operational Boundaries
- **AST Sandbox Limitation:** Static AST parsing verifies computational policies and rejects forbidden Python constructs; true process isolation requires OS containers.
- **Corpus Invariance:** Source documents are read-only and validated via SHA-256 baseline hashes.
- **Zero Secret Commitment:** Credentials must be provided via environment variables (`.env`).

---

## 12. Technical Documentation Index (`docs/`)
- `docs/BOOTSTRAP_DISCOVERY.md` — Initial workspace audit and baseline facts.
- `docs/ARCHITECTURE_DECISION.md` — ADR-001 adopting Option C Dual-Speed Engine.
- `docs/BENCHMARK_DATASET.md` — Specification and schema for the 30-case RAG benchmark dataset.
- `docs/RAG_BENCHMARK_REPORT.md` — Empirical IR and generation evaluation results on 30 benchmark cases.
- `docs/DUAL_SPEED_BENCHMARK.md` — Performance latency (100 warm runs), memory profiling, and ARS/MCTS bounds.
- `docs/SECURITY_VALIDATION_REPORT.md` — Detailed AST sandbox, execution policy, and injection resilience audit.
- `PHASE_2_ACCEPTANCE_REPORT.md` — Independent Phase 2 Production Readiness Acceptance Report.
- `docs/PROVIDER_CONFIGURATION.md` — LiteLLM and multi-provider setup.
- `docs/OPEN_DESIGN_QUESTIONS.md` — Audit of unverified theoretical claims.
- `docs/DEVELOPMENT.md` — Developer onboarding and coding guidelines.
- `docs/OPERATIONS.md` — Deployment and maintenance runbook.
- `docs/TESTING.md` — Test suite topology and verification procedures.
- `docs/SECURITY.md` — Threat model and AST policy boundaries.
- `docs/DECISION_LOG.md` — Chronological log of architectural decisions.
- `docs/TROUBLESHOOTING.md` — Diagnostic steps for common issues.

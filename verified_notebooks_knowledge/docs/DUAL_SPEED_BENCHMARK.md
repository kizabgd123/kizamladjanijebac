# HALO RAG Studio — Dual-Speed Benchmark Report

## 1. Executive Summary & Verification Verdict

The Option C Dual-Speed Architecture coordinates low-latency fast execution via `AgentReuseEngine` plan caching and progressive `ARSGate` checkpoints with rigorous multi-hop reasoning via `MCTSReasoner` and `ExecutionPolicyEngine`.

| Component / Subsystem | Status | Key Metric / Verification Finding |
|---|:---:|---|
| **Fast-Path Routing** | **PASS** | 100% cache hit rate on repeated queries; mean latency **4.47 ms** (p50: 4.29 ms, p95: 5.81 ms, p99: 7.11 ms). |
| **Deep-Path Execution** | **PASS** | Cold-start latency **98.76 ms** (includes MCTS tree search and plan caching). |
| **Paraphrase Discrimination** | **PASS** | Similarity threshold (0.92) correctly rejects paraphrases with low lexical overlap, routing to deep path (83.54 ms). |
| **ARS Checkpoint Gates** | **PASS WITH LIMITATIONS** | CP1 ($\tau_1=0.90$), CP2 ($\tau_2=0.85$), CP3 ($\tau_3=0.80$) gates operate deterministically with safety bypass; however, confidence scores are uncalibrated lexical heuristics. |
| **MCTS Tree Search** | **PASS** | Strict rollout depth ($\le 3$), bounded simulations ($N=8$), seed determinism (seed=42), and hard computational time-budget enforcement. |

---

## 2. Latency & Resource Utilization Profile (N=100 Warm Runs)

Empirical performance was benchmarked using Python `time.perf_counter()` and `tracemalloc` across 100 consecutive invocations on the verified corpus.

| Metric | Measured Value | Target SLA / Upper Bound |
|---|:---:|:---:|
| **Cold Start Latency** | **98.76 ms** | $\le 250\text{ ms}$ |
| **Warm Cache p50 (Median)** | **4.29 ms** | $\le 10\text{ ms}$ |
| **Warm Cache p95** | **5.81 ms** | $\le 20\text{ ms}$ |
| **Warm Cache p99** | **7.11 ms** | $\le 50\text{ ms}$ |
| **Warm Cache Mean** | **4.47 ms $\pm$ 0.64 ms** | $\le 15\text{ ms}$ |
| **Cache Hit Rate** | **100.0% (100/100)** | $\ge 90\%$ |
| **Peak Traced Memory (`tracemalloc`)** | **53.62 KB** | $\le 10\text{ MB}$ |
| **Current Traced Memory** | **12.63 KB** | — |

---

## 3. ARS Checkpoint Analysis & Confidence Calibration

### 3.1 Checkpoint Threshold Specifications
- **Checkpoint 1 (Surface / Intent Certainty)**: $\tau_1 = 0.90$. Evaluates lexical bigram cosine similarity between incoming query and cached plan intents.
- **Checkpoint 2 (Retrieval Relevance Certainty)**: $\tau_2 = 0.85$. Determines whether context retrieval confidence warrants direct synthesis without MCTS reasoning.
- **Checkpoint 3 (Answer Faithfulness Certainty)**: $\tau_3 = 0.80$. Assesses post-synthesis citation grounding before committing response.

### 3.2 Safety Bypass Verification
- When `metadata={"is_safety_critical": True}` or keywords like `delete`, `drop`, `credential`, `sudo` are detected, early exit is inhibited even if intent confidence $= 0.99$.
- Safety bypass was empirically verified: `cp1_safety_bypass = True` with `should_early_exit = False`.

### 3.3 Critical Limitation: Heuristic Confidence vs Statistical Calibration
> [!WARNING]
> While ARS thresholds operate deterministically as boolean gates, the underlying confidence values are **not statistically calibrated probabilities**:
> 1. CP1 confidence is derived strictly from lexical term and bigram overlap in SQLite-backed `AgentReuseEngine`.
> 2. CP2 and CP3 confidence values must be supplied externally by calling harnesses; they are not dynamically inferred through semantic calibration curves or conformal prediction.

---

## 4. MCTS Reasoner Bounds & Determinism Audit

### 4.1 Parameter Bounds Verification
- **Rollout Depth Bound**: Configured to $3$. Verified that generated trajectories never exceed length 3 (actual: 3).
- **Simulations Bound**: Configured to $8$. Verified root visits equal exactly 8.
- **Random Seed Determinism**: Verified that two distinct instances initialized with `random_seed=42` produce identical trajectories and identical best evaluation values ($0.8500$).
- **Time Budget Enforcement**: Verified that configuring `max_budget_ms=2` terminates MCTS search within $2.02\text{ ms}$ without throwing unhandled exceptions.

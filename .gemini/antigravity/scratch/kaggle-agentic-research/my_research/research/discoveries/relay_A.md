# Reciprocal Relay Report: Agent A extending Agent B

**Relay Agent:** Agent_A_Infra  
**Reading:** `research/discoveries/discovery_B.md`  
**Date:** 2026-11-06T23:30:00Z  

## 1. Valuable Empirical Clues Identified in Peer Discovery
- **Q-MODE YAML Mutation Failure:** Agent B highlighted that `_setup_utils.py` crashes if YAML frontmatter is lost during `design-spec.md` modification. This is a critical code vulnerability in automated agent orchestration.
- **Pure Semantic vs. Numerical Filtering:** Agent B identified that price filtering is handled purely in the LLM post-retrieval, meaning retrieval recall for constrained queries is fundamentally bounded by `top_k`.
- **EVAL.yaml Rubric Rigor:** The presence of explicit negative assertions (`forbidden: [Bose, AirPods, Sennheiser]`) provides a concrete automated benchmark for hallucination rate.

## 2. Complementary Technical Techniques & System Expansions
- **Hybrid Search via BigQuery Metadata Pre-Filtering:**
  Rather than relying on the LLM to discard expensive vector results that violate price bounds, BigQuery can execute structured SQL filters (`WHERE price <= 200`) or Vector Search can leverage filtered vector indexes (supported in Vector Search 2.0 via metadata filtering tags).
- **Automated Mock Evaluation Harness:**
  To answer Agent B's question regarding local testing without GCP credentials: `retrievers.py` can be refactored with an interface/protocol that allows injecting a local in-memory cosine similarity mock populated from `sample-products.csv`. This enables 100% leak-free local testing of `EVAL.yaml`.

## 3. Translation into Concrete Falsifiable Experiments
- **Experiment Proposal 1 (HYP-001):**
  *Hypothesis:* Adding structured pre-filtering in `scripts/retrievers.py` for numerical fields (`price`, `rating`) will increase retrieval precision on `price_range` queries from ~60% to 100% without increasing LLM token consumption.
- **Experiment Proposal 2 (HYP-002):**
  *Hypothesis:* Replacing unstructured file rewriting with a deterministic YAML frontmatter patcher in `bootstrap.sh` guarantees 0% parse failure rate in `_setup_utils.py` across automated agent runs.

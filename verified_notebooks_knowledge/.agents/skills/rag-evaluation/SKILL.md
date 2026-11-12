---
name: rag-evaluation
description: Evaluate RAG pipeline outputs using RAGAS 4-metric framework and composite quality gate.
---

# RAG Evaluation Skill

## When to Activate
Activate when benchmarking response quality, testing retrieval changes, or validating release readiness.

## Required Context
- Evaluator modules in `src/rag/metrics.py`.
- Benchmark evaluation questions and ground-truth contexts.
- Thresholds defined in `config/halo.yaml` (Composite Gate $\ge 0.80$).

## Execution Steps
1. Compute **Context Relevance** ($w=0.25$): assess signal-to-noise ratio in retrieved context chunks.
2. Compute **Answer Faithfulness** ($w=0.35$): assert factual consistency against retrieved context (zero hallucination).
3. Compute **Answer Relevance** ($w=0.25$): assess alignment of generated answer to the user query.
4. Compute **Noise Robustness** ($w=0.15$): test response stability against irrelevant or conflicting context.
5. Calculate composite quality score $Q_{rag} = \sum (w_i \cdot s_i)$.
6. Compare against quality gate threshold (0.80).

## Verification & Checks
- All metric values must fall within the normalized $[0.0, 1.0]$ range.
- Flag any individual failure in Answer Faithfulness regardless of composite score.

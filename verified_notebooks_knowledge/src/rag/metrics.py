"""
RAG Evaluation Metrics and Quality Gate for HALO RAG Studio.

Implements the 4-metric framework:
  1. Context Relevance (weight: 0.25)
  2. Answer Faithfulness (weight: 0.35)
  3. Answer Relevance (weight: 0.25)
  4. Noise Robustness (weight: 0.15)

Enforces Composite Quality Gate (Q_rag >= 0.80) and critical-metric safety floors.
"""

import collections
import math
import re
from typing import Any, Dict, List, Optional


class RAGEvalScores:
    def __init__(
        self,
        context_relevance: float,
        answer_faithfulness: float,
        answer_relevance: float,
        noise_robustness: float,
        weights: Optional[Dict[str, float]] = None,
        composite_gate_threshold: float = 0.80
    ):
        self.context_relevance = max(0.0, min(1.0, context_relevance))
        self.answer_faithfulness = max(0.0, min(1.0, answer_faithfulness))
        self.answer_relevance = max(0.0, min(1.0, answer_relevance))
        self.noise_robustness = max(0.0, min(1.0, noise_robustness))

        self.weights = weights or {
            "context_relevance": 0.25,
            "answer_faithfulness": 0.35,
            "answer_relevance": 0.25,
            "noise_robustness": 0.15
        }
        self.composite_gate_threshold = composite_gate_threshold

        # Calculate composite score
        self.composite_score = (
            self.weights["context_relevance"] * self.context_relevance +
            self.weights["answer_faithfulness"] * self.answer_faithfulness +
            self.weights["answer_relevance"] * self.answer_relevance +
            self.weights["noise_robustness"] * self.noise_robustness
        )

        # Critical floor check: Answer Faithfulness must not be below 0.70
        self.faithfulness_floor_passed = self.answer_faithfulness >= 0.70
        self.passed_gate = (self.composite_score >= self.composite_gate_threshold) and self.faithfulness_floor_passed

    def to_dict(self) -> Dict[str, Any]:
        return {
            "context_relevance": round(self.context_relevance, 4),
            "answer_faithfulness": round(self.answer_faithfulness, 4),
            "answer_relevance": round(self.answer_relevance, 4),
            "noise_robustness": round(self.noise_robustness, 4),
            "composite_score": round(self.composite_score, 4),
            "gate_threshold": self.composite_gate_threshold,
            "passed_gate": self.passed_gate,
            "faithfulness_floor_passed": self.faithfulness_floor_passed
        }


class RAGMetricsEvaluator:
    """
    Computes deterministic lexical and semantic quality metrics across RAG inputs and outputs.
    """

    def __init__(
        self,
        composite_threshold: float = 0.80,
        weights: Optional[Dict[str, float]] = None
    ):
        self.composite_threshold = composite_threshold
        self.weights = weights or {
            "context_relevance": 0.25,
            "answer_faithfulness": 0.35,
            "answer_relevance": 0.25,
            "noise_robustness": 0.15
        }

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r"\w+", text.lower())

    def _overlap_ratio(self, text1: str, text2: str) -> float:
        t1 = set(self._tokenize(text1))
        t2 = set(self._tokenize(text2))
        if not t1 or not t2:
            return 0.0
        return len(t1 & t2) / min(len(t1), len(t2))

    def evaluate(
        self,
        query: str,
        retrieved_contexts: List[str],
        generated_answer: str,
        ground_truth: Optional[str] = None
    ) -> RAGEvalScores:
        if not retrieved_contexts or not generated_answer.strip():
            return RAGEvalScores(0.0, 0.0, 0.0, 0.0, self.weights, self.composite_threshold)

        combined_context = " ".join(retrieved_contexts)

        # 1. Context Relevance: Proportion of query concepts captured in retrieved context
        context_rel = min(1.0, self._overlap_ratio(query, combined_context) * 1.5)

        # 2. Answer Faithfulness: Proportion of answer assertions grounded in context
        faithfulness = self._overlap_ratio(generated_answer, combined_context)

        # 3. Answer Relevance: Semantic overlap between answer and original user query
        answer_rel = self._overlap_ratio(query, generated_answer)

        # 4. Noise Robustness: Resistance to irrelevant chunks
        # If multiple chunks exist, test consistency
        if len(retrieved_contexts) > 1:
            chunk_sims = [self._overlap_ratio(retrieved_contexts[0], c) for c in retrieved_contexts[1:]]
            noise_rob = sum(chunk_sims) / len(chunk_sims)
        else:
            noise_rob = 0.90

        return RAGEvalScores(
            context_relevance=context_rel,
            answer_faithfulness=faithfulness,
            answer_relevance=answer_rel,
            noise_robustness=noise_rob,
            weights=self.weights,
            composite_gate_threshold=self.composite_threshold
        )

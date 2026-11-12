"""Unit tests for RAG evaluation metrics formulas and composite quality gates."""

import pytest
from src.rag.metrics import RAGEvalScores, RAGMetricsEvaluator


def test_composite_score_formula():
    scores = RAGEvalScores(
        context_relevance=1.0,
        answer_faithfulness=1.0,
        answer_relevance=1.0,
        noise_robustness=1.0,
        composite_gate_threshold=0.80
    )
    # 0.25*1.0 + 0.35*1.0 + 0.25*1.0 + 0.15*1.0 = 1.0
    assert pytest.approx(scores.composite_score, 0.001) == 1.0
    assert scores.passed_gate is True
    assert scores.faithfulness_floor_passed is True


def test_faithfulness_critical_floor_rejection():
    # Even if other scores are high, faithfulness < 0.70 must fail the quality gate
    scores = RAGEvalScores(
        context_relevance=1.0,
        answer_faithfulness=0.60,
        answer_relevance=1.0,
        noise_robustness=1.0,
        composite_gate_threshold=0.80
    )
    # composite = 0.25*1 + 0.35*0.60 + 0.25*1 + 0.15*1 = 0.25 + 0.21 + 0.25 + 0.15 = 0.86
    assert scores.composite_score >= 0.80
    assert scores.faithfulness_floor_passed is False
    assert scores.passed_gate is False  # Rejected because of faithfulness floor violation


def test_evaluator_lexical_calculations():
    evaluator = RAGMetricsEvaluator()
    query = "Kako radi neuronska mreza"
    retrieved = [
        "Neuronska mreza funkcionise pomocu slojeva i tezina.",
        "Neuronska mreza i duboko ucenje koriste vise slojeva."
    ]
    answer = "Neuronska mreza funkcionise kroz slojeve i tezine za ucenje."

    result = evaluator.evaluate(query, retrieved, answer)
    assert result.context_relevance > 0.0
    assert result.answer_faithfulness > 0.0
    assert result.answer_relevance > 0.0
    assert result.noise_robustness > 0.0

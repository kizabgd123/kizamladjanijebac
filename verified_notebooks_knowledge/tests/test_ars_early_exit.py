"""Unit tests for Adaptive Reasoning Suppression (ARS) multi-checkpoint gate."""

import pytest
from src.core.ars_gate import ARSDecision, ARSGate


@pytest.fixture
def ars():
    return ARSGate(tau_1=0.90, tau_2=0.85, tau_3=0.80)


def test_checkpoint_1_early_exit(ars):
    decision = ars.evaluate_checkpoint_1(intent_confidence=0.95, query="Zdravo, sta je CodyMaster?")
    assert decision.should_early_exit is True
    assert decision.checkpoint == 1
    assert decision.confidence == 0.95


def test_checkpoint_1_escalation(ars):
    decision = ars.evaluate_checkpoint_1(intent_confidence=0.82, query="Kompleksno pitanje...")
    assert decision.should_early_exit is False
    assert decision.checkpoint == 1
    assert "below threshold" in decision.reason


def test_checkpoint_2_early_exit(ars):
    decision = ars.evaluate_checkpoint_2(retrieval_relevance=0.88, candidate_count=3)
    assert decision.should_early_exit is True
    assert decision.checkpoint == 2


def test_checkpoint_2_escalation(ars):
    decision = ars.evaluate_checkpoint_2(retrieval_relevance=0.75, candidate_count=1)
    assert decision.should_early_exit is False
    assert decision.checkpoint == 2


def test_checkpoint_3_synthesis_commit(ars):
    decision = ars.evaluate_checkpoint_3(faithfulness_score=0.84)
    assert decision.should_early_exit is True
    assert decision.checkpoint == 3


def test_checkpoint_3_overthinking_rejection(ars):
    decision = ars.evaluate_checkpoint_3(faithfulness_score=0.65)
    assert decision.should_early_exit is False
    assert decision.checkpoint == 3


def test_safety_critical_bypass(ars):
    # Destructive or security sensitive operations must bypass early exit even with 1.0 confidence
    decision = ars.evaluate_checkpoint_1(intent_confidence=1.0, query="sudo rm -rf /home/data")
    assert decision.should_early_exit is False
    assert "Critical risk" in decision.reason


def test_invalid_confidence_values(ars):
    # Out of bounds confidence handled safely
    dec_neg = ars.evaluate_checkpoint_1(intent_confidence=-0.5, query="test")
    assert dec_neg.should_early_exit is False
    assert dec_neg.confidence == 0.0

    dec_high = ars.evaluate_checkpoint_1(intent_confidence=1.5, query="test")
    assert dec_high.confidence == 1.0

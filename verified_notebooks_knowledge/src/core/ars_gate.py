"""
Adaptive Reasoning Suppression (ARS) Certainty Gate.

Evaluates 3 progressive checkpoints:
  - Checkpoint 1: Surface/Intent Certainty (tau_1 = 0.90)
  - Checkpoint 2: Retrieval Relevance Certainty (tau_2 = 0.85)
  - Checkpoint 3: Answer Faithfulness Certainty (tau_3 = 0.80)

Enforces safety bypass: security-critical intents, external side effects,
or contradictory evidence force full Deep-Path reasoning regardless of scores.
"""

from enum import IntEnum
from typing import Any, Dict, List, Optional


class ARSCheckpoint(IntEnum):
    INTENT = 1
    RETRIEVAL = 2
    SYNTHESIS = 3


class ARSDecision:
    def __init__(
        self,
        checkpoint: ARSCheckpoint,
        score: float,
        threshold: float,
        should_early_exit: bool,
        reason: str,
        safety_bypass_active: bool = False
    ):
        self.checkpoint = checkpoint
        self.score = score
        self.confidence = score
        self.threshold = threshold
        self.should_early_exit = should_early_exit
        self.reason = reason
        self.safety_bypass_active = safety_bypass_active

    def to_dict(self) -> Dict[str, Any]:
        return {
            "checkpoint": self.checkpoint.name,
            "score": round(self.score, 4),
            "confidence": round(self.confidence, 4),
            "threshold": self.threshold,
            "should_early_exit": self.should_early_exit,
            "reason": self.reason,
            "safety_bypass_active": self.safety_bypass_active
        }


class ARSGate:
    """
    Evaluates progressive certainty thresholds and enforces safety critical bypasses.
    """

    CRITICAL_KEYWORDS = {
        "delete", "rm", "drop", "sudo", "truncate", "overwrite",
        "destroy", "kill", "privilege", "credential", "password",
        "secret", "token", "auth", "bypass", "exploit"
    }

    def __init__(
        self,
        tau_1_intent: Optional[float] = None,
        tau_2_retrieval: Optional[float] = None,
        tau_3_faithfulness: Optional[float] = None,
        tau_1: Optional[float] = None,
        tau_2: Optional[float] = None,
        tau_3: Optional[float] = None,
        enabled: bool = True
    ):
        self.tau_1 = tau_1 if tau_1 is not None else (tau_1_intent if tau_1_intent is not None else 0.90)
        self.tau_2 = tau_2 if tau_2 is not None else (tau_2_retrieval if tau_2_retrieval is not None else 0.85)
        self.tau_3 = tau_3 if tau_3 is not None else (tau_3_faithfulness if tau_3_faithfulness is not None else 0.80)
        self.enabled = enabled

    def check_safety_bypass(self, query: str, metadata: Optional[Dict[str, Any]] = None) -> bool:
        """
        Returns True if the query triggers safety-critical bypass rules.
        """
        tokens = query.lower().split()
        for token in tokens:
            if token in self.CRITICAL_KEYWORDS:
                return True

        if metadata:
            if metadata.get("is_safety_critical", False):
                return True
            if metadata.get("has_conflicting_evidence", False):
                return True
            if metadata.get("destructive_operation", False):
                return True

        return False

    def evaluate_checkpoint_1(
        self,
        intent_confidence: float,
        query: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> ARSDecision:
        """
        Checkpoint 1: Surface / Intent Certainty.
        Determines whether simple conversational queries or direct lookups can exit immediately.
        """
        clamped_conf = max(0.0, min(1.0, intent_confidence))
        if not self.enabled:
            return ARSDecision(ARSCheckpoint.INTENT, clamped_conf, self.tau_1, False, "ARS disabled")

        if self.check_safety_bypass(query, metadata):
            return ARSDecision(
                ARSCheckpoint.INTENT, clamped_conf, self.tau_1, False,
                "Critical risk: sensitive query requires Deep-Path analysis",
                safety_bypass_active=True
            )

        if clamped_conf >= self.tau_1:
            return ARSDecision(
                ARSCheckpoint.INTENT, clamped_conf, self.tau_1, True,
                f"Intent confidence {clamped_conf:.2f} >= tau_1 ({self.tau_1}): early exit granted"
            )

        return ARSDecision(
            ARSCheckpoint.INTENT, clamped_conf, self.tau_1, False,
            f"Intent confidence {clamped_conf:.2f} below threshold tau_1 ({self.tau_1}): proceed to retrieval"
        )

    def evaluate_checkpoint_2(
        self,
        retrieval_relevance_score: Optional[float] = None,
        query: str = "",
        metadata: Optional[Dict[str, Any]] = None,
        retrieval_relevance: Optional[float] = None,
        candidate_count: int = 1
    ) -> ARSDecision:
        """
        Checkpoint 2: Retrieval Relevance Certainty.
        Determines whether high-confidence retrieved context is sufficient for direct synthesis
        without launching full MCTS multi-hop reasoning.
        """
        score = retrieval_relevance if retrieval_relevance is not None else (retrieval_relevance_score or 0.0)
        clamped_score = max(0.0, min(1.0, score))

        if not self.enabled:
            return ARSDecision(ARSCheckpoint.RETRIEVAL, clamped_score, self.tau_2, False, "ARS disabled")

        if query and self.check_safety_bypass(query, metadata):
            return ARSDecision(
                ARSCheckpoint.RETRIEVAL, clamped_score, self.tau_2, False,
                "Critical risk: sensitive or conflicting retrieval requires Deep-Path",
                safety_bypass_active=True
            )

        if clamped_score >= self.tau_2:
            return ARSDecision(
                ARSCheckpoint.RETRIEVAL, clamped_score, self.tau_2, True,
                f"Retrieval relevance {clamped_score:.2f} >= tau_2 ({self.tau_2}): skip MCTS reasoning"
            )

        return ARSDecision(
            ARSCheckpoint.RETRIEVAL, clamped_score, self.tau_2, False,
            f"Retrieval relevance {clamped_score:.2f} below threshold tau_2 ({self.tau_2}): invoke MCTS deep reasoning"
        )

    def evaluate_checkpoint_3(
        self,
        faithfulness_score: float = 0.0,
        query: str = "",
        metadata: Optional[Dict[str, Any]] = None
    ) -> ARSDecision:
        """
        Checkpoint 3: Answer Faithfulness Certainty.
        Determines whether synthesized answer is grounded firmly enough to commit
        without redundant post-synthesis verification hops.
        """
        clamped_score = max(0.0, min(1.0, faithfulness_score))

        if not self.enabled:
            return ARSDecision(ARSCheckpoint.SYNTHESIS, clamped_score, self.tau_3, False, "ARS disabled")

        if clamped_score >= self.tau_3:
            return ARSDecision(
                ARSCheckpoint.SYNTHESIS, clamped_score, self.tau_3, True,
                f"Faithfulness {clamped_score:.2f} >= tau_3 ({self.tau_3}): commit answer"
            )

        return ARSDecision(
            ARSCheckpoint.SYNTHESIS, clamped_score, self.tau_3, False,
            f"Faithfulness {clamped_score:.2f} below threshold tau_3 ({self.tau_3}): trigger regeneration or rollback"
        )

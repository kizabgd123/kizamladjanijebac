"""
Execution Policy Engine for HALO RAG Studio.

Evaluates user query risk, permissions, and environmental constraints
to determine whether execution proceeds via Fast-Path, Deep-Path, or is Rejected.
"""

from enum import Enum
from typing import Any, Dict, List, Optional


class RoutingChannel(Enum):
    FAST_PATH = "fast_path"
    DEEP_PATH = "deep_path"
    REJECT = "reject"


class ExecutionPolicyDecision:
    def __init__(
        self,
        channel: RoutingChannel,
        is_safe: bool,
        reasons: List[str],
        risk_score: float = 0.0,
        metadata: Optional[Dict[str, Any]] = None
    ):
        self.channel = channel
        self.is_safe = is_safe
        self.reasons = reasons
        self.risk_score = risk_score
        self.metadata = metadata or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "channel": self.channel.value,
            "is_safe": self.is_safe,
            "reasons": self.reasons,
            "risk_score": round(self.risk_score, 3),
            "metadata": self.metadata
        }


class ExecutionPolicyEngine:
    """
    Evaluates query and context risks against immutable system laws.
    """

    CRITICAL_RISK_PATTERNS = [
        "rm -rf", "sudo ", "mkfs", "dd if=", ":(){ :|:& };:",
        "drop database", "truncate table", "> /dev/sda"
    ]

    HIGH_RISK_KEYWORDS = [
        "password", "secret", "credential", "auth_token", "private_key",
        "api_key", "chmod 777", "exec(", "eval("
    ]

    def evaluate(
        self,
        query: str,
        corpus_valid: bool = True,
        metadata: Optional[Dict[str, Any]] = None
    ) -> ExecutionPolicyDecision:
        reasons: List[str] = []
        risk_score = 0.0
        q_lower = query.lower()

        # Check immutable law 1: Destructive OS commands
        for pattern in self.CRITICAL_RISK_PATTERNS:
            if pattern in q_lower:
                reasons.append(f"Forbidden destructive command pattern detected: '{pattern}'")
                return ExecutionPolicyDecision(
                    channel=RoutingChannel.REJECT,
                    is_safe=False,
                    reasons=reasons,
                    risk_score=1.0
                )

        # Check corpus validity
        if not corpus_valid:
            reasons.append("Corpus hash integrity check failed or unverified")
            return ExecutionPolicyDecision(
                channel=RoutingChannel.REJECT,
                is_safe=False,
                reasons=reasons,
                risk_score=0.9
            )

        # Check high-risk keywords
        for kw in self.HIGH_RISK_KEYWORDS:
            if kw in q_lower:
                risk_score += 0.3
                reasons.append(f"High-risk keyword identified: '{kw}'")

        if risk_score >= 0.6:
            reasons.append("Elevated risk threshold reached; routing strictly to Deep-Path with human oversight")
            return ExecutionPolicyDecision(
                channel=RoutingChannel.DEEP_PATH,
                is_safe=True,
                reasons=reasons,
                risk_score=risk_score
            )

        reasons.append("Standard safe inquiry: Fast-Path eligibility granted")
        return ExecutionPolicyDecision(
            channel=RoutingChannel.FAST_PATH,
            is_safe=True,
            reasons=reasons,
            risk_score=risk_score
        )

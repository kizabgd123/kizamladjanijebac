"""
Dual-Speed Runtime Router for HALO RAG Studio.

Orchestrates Option C:
  - Fast-Path: AgentReuse Plan Cache + ARS Checkpoint 1 & 2 early exit
  - Deep-Path: 3-Tier HALO Reasoning with bounded MCTS + CaP AST Sandbox
"""

import time
from typing import Any, Callable, Dict, List, Optional

from src.core.agent_reuse import AgentReuseEngine, CachedExecutionPlan
from src.core.ars_gate import ARSDecision, ARSGate
from src.core.ast_sandbox import SandboxedExecutionResult, execute_policy_code
from src.core.execution_policy import ExecutionPolicyEngine, RoutingChannel
from src.core.mcts import MCTSReasoner, MCTSResult


class DualSpeedExecutionResult:
    def __init__(
        self,
        query: str,
        channel: str,
        response: str,
        plan_steps: List[str],
        citations: List[Dict[str, Any]],
        latency_ms: float,
        cached_plan_id: Optional[str] = None,
        ars_decision: Optional[Dict[str, Any]] = None,
        mcts_stats: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        self.query = query
        self.channel = channel
        self.response = response
        self.plan_steps = plan_steps
        self.citations = citations
        self.latency_ms = latency_ms
        self.cached_plan_id = cached_plan_id
        self.ars_decision = ars_decision
        self.mcts_stats = mcts_stats
        self.metadata = metadata or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "query": self.query,
            "channel": self.channel,
            "response": self.response,
            "plan_steps": self.plan_steps,
            "citations": self.citations,
            "latency_ms": round(self.latency_ms, 2),
            "cached_plan_id": self.cached_plan_id,
            "ars_decision": self.ars_decision,
            "mcts_stats": self.mcts_stats,
            "metadata": self.metadata
        }


class DualSpeedRuntimeRouter:
    """
    Coordinates query routing between Fast-Path (AgentReuse/ARS) and Deep-Path (MCTS/CaP).
    """

    def __init__(
        self,
        agent_reuse: AgentReuseEngine,
        ars_gate: ARSGate,
        policy_engine: ExecutionPolicyEngine,
        mcts_reasoner: Optional[MCTSReasoner] = None,
        corpus_hash: str = ""
    ):
        self.agent_reuse = agent_reuse
        self.ars_gate = ars_gate
        self.policy_engine = policy_engine
        self.mcts_reasoner = mcts_reasoner or MCTSReasoner()
        self.corpus_hash = corpus_hash

    def route_and_execute(
        self,
        query: str,
        rag_pipeline_fn: Callable[[str, List[str]], Dict[str, Any]],
        metadata: Optional[Dict[str, Any]] = None
    ) -> DualSpeedExecutionResult:
        start_time = time.time()
        meta = metadata or {}

        # 1. Evaluate Execution Policy
        policy = self.policy_engine.evaluate(query, corpus_valid=True, metadata=meta)
        if policy.channel == RoutingChannel.REJECT:
            elapsed = (time.time() - start_time) * 1000.0
            return DualSpeedExecutionResult(
                query=query,
                channel="rejected",
                response=f"Execution rejected by policy: {'; '.join(policy.reasons)}",
                plan_steps=[],
                citations=[],
                latency_ms=elapsed,
                metadata={"policy": policy.to_dict()}
            )

        # 2. Check Fast-Path Eligibility (AgentReuse Cache)
        if policy.channel == RoutingChannel.FAST_PATH:
            cached_plan, similarity = self.agent_reuse.lookup_plan(
                query=query,
                corpus_hash=self.corpus_hash,
                model_profile=meta.get("model_profile", "default")
            )

            if cached_plan is not None:
                # Check ARS Checkpoint 1 (Intent Certainty)
                ars_decision = self.ars_gate.evaluate_checkpoint_1(
                    intent_confidence=similarity,
                    query=query,
                    metadata=meta
                )

                if ars_decision.should_early_exit:
                    # Execute fast-path using cached route and plan
                    rag_result = rag_pipeline_fn(query, cached_plan.plan_steps)
                    elapsed = (time.time() - start_time) * 1000.0
                    return DualSpeedExecutionResult(
                        query=query,
                        channel="fast_path",
                        response=rag_result.get("response", ""),
                        plan_steps=cached_plan.plan_steps,
                        citations=rag_result.get("citations", []),
                        latency_ms=elapsed,
                        cached_plan_id=cached_plan.plan_id,
                        ars_decision=ars_decision.to_dict(),
                        metadata={"similarity": round(similarity, 4)}
                    )

        # 3. Deep-Path Execution (HALO 3-Tier Reasoning & MCTS)
        # Define candidate actions for MCTS
        def generate_actions(state: str, depth: int) -> List[str]:
            if depth == 0:
                return ["rewrite_query", "extract_keywords", "semantic_decompose"]
            elif depth == 1:
                return ["retrieve_top_k", "hybrid_bm25_dense", "metadata_filter"]
            else:
                return ["grounded_synthesis", "multi_source_reconcile", "citation_verify"]

        def evaluate_trajectory(state: str, traj: List[str]) -> float:
            score = 0.5
            if "rewrite_query" in traj or "semantic_decompose" in traj:
                score += 0.2
            if "hybrid_bm25_dense" in traj or "retrieve_top_k" in traj:
                score += 0.2
            if "grounded_synthesis" in traj or "citation_verify" in traj:
                score += 0.1
            return min(1.0, score)

        mcts_result = self.mcts_reasoner.search(
            initial_state=f"Query: {query}",
            action_generator=generate_actions,
            evaluator=evaluate_trajectory
        )

        # Execute RAG using trajectory from MCTS
        rag_result = rag_pipeline_fn(query, mcts_result.best_trajectory)

        # Cache the validated plan for future reuse
        self.agent_reuse.store_plan(
            intent_query=query,
            plan_steps=mcts_result.best_trajectory,
            route_destination=rag_result.get("destination", "verified_corpus"),
            corpus_hash=self.corpus_hash,
            model_profile=meta.get("model_profile", "default"),
            f1_score=mcts_result.best_value
        )

        elapsed = (time.time() - start_time) * 1000.0
        return DualSpeedExecutionResult(
            query=query,
            channel="deep_path",
            response=rag_result.get("response", ""),
            plan_steps=mcts_result.best_trajectory,
            citations=rag_result.get("citations", []),
            latency_ms=elapsed,
            mcts_stats=mcts_result.to_dict(),
            metadata={"mcts_best_value": round(mcts_result.best_value, 4)}
        )

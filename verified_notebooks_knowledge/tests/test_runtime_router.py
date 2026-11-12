"""Unit tests for Dual-Speed Runtime Router (Fast-Path vs Deep-Path)."""

import pytest
from src.core.agent_reuse import AgentReuseEngine
from src.core.ars_gate import ARSGate
from src.core.execution_policy import ExecutionPolicyEngine
from src.core.runtime_router import DualSpeedRuntimeRouter


@pytest.fixture
def dual_router(tmp_path):
    db_file = str(tmp_path / "router_test.db")
    agent_reuse = AgentReuseEngine(db_path=db_file, similarity_threshold=0.85)
    ars_gate = ARSGate()
    policy_engine = ExecutionPolicyEngine()
    return DualSpeedRuntimeRouter(agent_reuse, ars_gate, policy_engine)


def test_dual_speed_routing_fast_and_deep_path(dual_router):
    query = "Kako radi CodyMaster deterministicki RAG?"

    def mock_rag(q, steps):
        return {"response": "Mock RAG response grounded in corpus.", "citations": ["05_CodyMaster.md"]}

    # First execution: Cache miss -> Deep-Path (MCTS reasoning + RAG)
    res_deep = dual_router.route_and_execute(query, mock_rag)
    assert res_deep.channel == "deep_path"
    assert len(res_deep.plan_steps) > 0
    assert res_deep.response == "Mock RAG response grounded in corpus."

    # Second execution of same query: Cache hit -> Fast-Path (ARS Checkpoint 1 early exit)
    res_fast = dual_router.route_and_execute(query, mock_rag)
    assert res_fast.channel == "fast_path"
    assert res_fast.cached_plan_id is not None
    assert res_fast.latency_ms >= 0.0


def test_safety_critical_rejection_and_deep_path(dual_router):
    # Destructive operations must be rejected outright
    destructive_query = "sudo rm -rf system files"
    res_dest = dual_router.route_and_execute(destructive_query, lambda q, s: {"response": "", "citations": []})
    assert res_dest.channel == "rejected"

    # High-risk operations (e.g. secret/credential) must force deep-path
    high_risk_query = "Kako zastititi api_key i secret password u produkciji?"

    def mock_rag(q, steps):
        return {"response": "Refused dangerous operation or executed under deep inspection.", "citations": []}

    res_risk = dual_router.route_and_execute(high_risk_query, mock_rag)
    assert res_risk.channel == "deep_path"

#!/usr/bin/env python3
"""Quick sanity check for ModularRAGPipeline and DualSpeedRuntimeRouter."""
import sys
import os
sys.path.insert(0, os.path.abspath("."))

from src.rag.pipeline import ModularRAGPipeline
from src.core.agent_reuse import AgentReuseEngine
from src.core.ars_gate import ARSGate
from src.core.execution_policy import ExecutionPolicyEngine
from src.core.mcts import MCTSReasoner
from src.core.runtime_router import DualSpeedRuntimeRouter

def main():
    print("Initializing Modular RAG Pipeline...")
    pipe = ModularRAGPipeline()
    print(f"Indexed {len(pipe.documents)} documents into {len(pipe.chunks)} chunks.")

    query = "Kako radi CodyMaster deterministicki RAG pajplajn?"
    print(f"\nTesting Query: '{query}'")
    result = pipe.execute_query(query)
    print(f"Route: {result['route']['category']} (Confidence: {result['route']['confidence']})")
    print(f"Grounded: {result['grounded']}, Citations count: {len(result['citations'])}")
    print(f"Evaluation Composite Score: {result['evaluation']['composite_score']} (Passed Gate: {result['evaluation']['passed_gate']})")
    print("\nResponse Preview:\n" + result['response'][:250] + "...")

    print("\nInitializing Dual-Speed Runtime Router...")
    agent_reuse = AgentReuseEngine(db_path="data/test_agent_reuse.db")
    ars_gate = ARSGate()
    policy_engine = ExecutionPolicyEngine()
    router = DualSpeedRuntimeRouter(agent_reuse, ars_gate, policy_engine)

    def rag_fn(q, steps):
        return pipe.execute_query(q)

    # First run: Deep-Path (no cache)
    res1 = router.route_and_execute(query, rag_fn)
    print(f"\nRun 1 Channel: {res1.channel} (Latency: {res1.latency_ms} ms)")

    # Second run: Fast-Path (cached)
    res2 = router.route_and_execute(query, rag_fn)
    print(f"Run 2 Channel: {res2.channel} (Latency: {res2.latency_ms} ms, Plan ID: {res2.cached_plan_id})")

    if res2.channel == "fast_path":
        print("✅ Dual-Speed Fast-Path caching verified successfully!")
    else:
        print("❌ Fast-path failed to activate on repeated query!")
        sys.exit(1)

if __name__ == "__main__":
    main()

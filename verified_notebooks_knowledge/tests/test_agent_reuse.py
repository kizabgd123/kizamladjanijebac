"""Unit tests for AgentReuse semantic intent caching and plan reuse."""

import os
import time
import pytest
from src.core.agent_reuse import AgentReuseEngine, CachedExecutionPlan, compute_text_similarity


@pytest.fixture
def temp_cache_engine(tmp_path):
    db_file = str(tmp_path / "test_reuse.db")
    engine = AgentReuseEngine(
        db_path=db_file,
        similarity_threshold=0.85,
        ttl_seconds=2,
        current_corpus_hash="hash_baseline_v1"
    )
    return engine


def test_compute_text_similarity():
    sim_exact = compute_text_similarity("Kako radi CodyMaster deterministicki RAG", "Kako radi CodyMaster deterministicki RAG")
    assert sim_exact == 1.0

    sim_similar = compute_text_similarity("Kako radi CodyMaster deterministicki RAG", "CodyMaster deterministicki RAG objasnjenje")
    assert sim_similar > 0.50

    sim_diff = compute_text_similarity("Kako trenirati neuronsku mrezu", "Kako skuvati kafu")
    assert sim_diff < 0.20


def test_agent_reuse_store_and_hit(temp_cache_engine):
    engine = temp_cache_engine
    plan = engine.store_plan(
        intent_query="Objasni CodyMaster RAG",
        plan_steps=["route", "retrieve", "synthesize"],
        route_destination="05_CodyMaster",
        corpus_hash="hash_baseline_v1",
        f1_score=0.98
    )

    # Exact lookup
    hit_plan, score = engine.lookup_plan("Objasni CodyMaster RAG")
    assert hit_plan is not None
    assert hit_plan.plan_id == plan.plan_id
    assert hit_plan.plan_steps == ["route", "retrieve", "synthesize"]
    assert score == 1.0
    assert engine.stats["hits"] == 1


def test_agent_reuse_miss(temp_cache_engine):
    engine = temp_cache_engine
    hit_plan, score = engine.lookup_plan("Potpuno nepoznato pitanje o kvantnoj fizici")
    assert hit_plan is None
    assert engine.stats["misses"] == 1


def test_agent_reuse_ttl_expiration(temp_cache_engine):
    engine = temp_cache_engine
    engine.store_plan(
        intent_query="Privremeni upit",
        plan_steps=["step1"],
        route_destination="dest",
        corpus_hash="hash_baseline_v1"
    )

    # Immediately available
    plan, _ = engine.lookup_plan("Privremeni upit")
    assert plan is not None

    # Fast forward time beyond TTL (2 seconds)
    future_time = time.time() + 5.0
    expired_plan, _ = engine.lookup_plan("Privremeni upit", current_time=future_time)
    assert expired_plan is None
    assert engine.stats["stale_invalidations"] >= 1


def test_agent_reuse_stale_corpus_invalidation(temp_cache_engine):
    engine = temp_cache_engine
    engine.store_plan(
        intent_query="Pitanje o svesci 4",
        plan_steps=["sveska_4"],
        route_destination="04_Antigravity",
        corpus_hash="hash_baseline_v1"
    )

    # Change corpus hash to simulate knowledge base update
    plan_stale, _ = engine.lookup_plan("Pitanje o svesci 4", corpus_hash="hash_updated_v2")
    assert plan_stale is None
    assert engine.stats["stale_invalidations"] >= 1


def test_persistent_cache_recovery(tmp_path):
    db_file = str(tmp_path / "persistent_test.db")
    engine1 = AgentReuseEngine(db_path=db_file, current_corpus_hash="h1")
    engine1.store_plan(
        intent_query="Persisted Query",
        plan_steps=["stepA", "stepB"],
        route_destination="destA",
        corpus_hash="h1"
    )

    # Instantiate new engine instance pointing to the same SQLite DB
    engine2 = AgentReuseEngine(db_path=db_file, current_corpus_hash="h1")
    recovered, score = engine2.lookup_plan("Persisted Query")
    assert recovered is not None
    assert recovered.intent_query == "Persisted Query"
    assert recovered.plan_steps == ["stepA", "stepB"]

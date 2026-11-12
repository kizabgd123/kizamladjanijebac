"""
AgentReuse: Semantic Intent Caching and Plan Reuse Engine.

Provides dual-layer caching (in-memory LRU + persistent SQLite), TTL invalidation,
corpus version awareness, and semantic similarity thresholding (sigma >= 0.92).
"""

import collections
import hashlib
import json
import math
import os
import re
import sqlite3
import time
from typing import Any, Dict, List, Optional, Tuple


def compute_text_similarity(text1: str, text2: str) -> float:
    """
    Computes a deterministic cosine similarity over normalized character/word n-gram frequencies.
    Acts as an offline semantic similarity fallback when dense neural embeddings are unavailable.
    """
    def tokenize(t: str) -> collections.Counter:
        words = re.findall(r"\w+", t.lower())
        bigrams = [f"{words[i]}_{words[i+1]}" for i in range(len(words)-1)]
        return collections.Counter(words + bigrams)

    vec1 = tokenize(text1)
    vec2 = tokenize(text2)

    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum(vec1[x] * vec2[x] for x in intersection)

    sum1 = sum(v**2 for v in vec1.values())
    sum2 = sum(v**2 for v in vec2.values())
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    return float(numerator) / denominator


class CachedExecutionPlan:
    def __init__(
        self,
        plan_id: str,
        intent_query: str,
        plan_steps: List[str],
        route_destination: str,
        corpus_hash: str,
        model_profile: str,
        created_at: float,
        ttl_seconds: int = 86400,
        f1_score: float = 1.0,
        metadata: Optional[Dict[str, Any]] = None
    ):
        self.plan_id = plan_id
        self.intent_query = intent_query
        self.plan_steps = plan_steps
        self.route_destination = route_destination
        self.corpus_hash = corpus_hash
        self.model_profile = model_profile
        self.created_at = created_at
        self.ttl_seconds = ttl_seconds
        self.f1_score = f1_score
        self.metadata = metadata or {}

    def is_expired(self, current_time: Optional[float] = None) -> bool:
        now = current_time if current_time is not None else time.time()
        return (now - self.created_at) > self.ttl_seconds

    def to_dict(self) -> Dict[str, Any]:
        return {
            "plan_id": self.plan_id,
            "intent_query": self.intent_query,
            "plan_steps": self.plan_steps,
            "route_destination": self.route_destination,
            "corpus_hash": self.corpus_hash,
            "model_profile": self.model_profile,
            "created_at": self.created_at,
            "ttl_seconds": self.ttl_seconds,
            "f1_score": self.f1_score,
            "metadata": self.metadata
        }


class AgentReuseEngine:
    """
    Fast-path cache coordinator managing in-memory LRU and persistent SQLite storage.
    """

    def __init__(
        self,
        db_path: str = "data/agent_reuse_cache.db",
        similarity_threshold: float = 0.92,
        ttl_seconds: int = 86400,
        max_lru_items: int = 500,
        current_corpus_hash: str = ""
    ):
        self.db_path = db_path
        self.similarity_threshold = similarity_threshold
        self.ttl_seconds = ttl_seconds
        self.max_lru_items = max_lru_items
        self.current_corpus_hash = current_corpus_hash
        self.lru_cache: collections.OrderedDict[str, CachedExecutionPlan] = collections.OrderedDict()

        # Telemetry metrics
        self.stats = {
            "hits": 0,
            "misses": 0,
            "evictions": 0,
            "stale_invalidations": 0
        }

        os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
        self._init_sqlite()

    def _init_sqlite(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS plan_cache (
                    plan_id TEXT PRIMARY KEY,
                    intent_query TEXT NOT NULL,
                    plan_steps_json TEXT NOT NULL,
                    route_destination TEXT NOT NULL,
                    corpus_hash TEXT NOT NULL,
                    model_profile TEXT NOT NULL,
                    created_at REAL NOT NULL,
                    ttl_seconds INTEGER NOT NULL,
                    f1_score REAL NOT NULL,
                    metadata_json TEXT
                )
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_corpus ON plan_cache(corpus_hash)")
            conn.commit()

    def _generate_plan_id(self, query: str, corpus_hash: str, model_profile: str) -> str:
        raw = f"{query.strip().lower()}::{corpus_hash}::{model_profile}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]

    def store_plan(
        self,
        intent_query: str,
        plan_steps: List[str],
        route_destination: str,
        corpus_hash: Optional[str] = None,
        model_profile: str = "default",
        f1_score: float = 1.0,
        metadata: Optional[Dict[str, Any]] = None
    ) -> CachedExecutionPlan:
        active_corpus_hash = corpus_hash or self.current_corpus_hash
        plan_id = self._generate_plan_id(intent_query, active_corpus_hash, model_profile)
        now = time.time()

        plan = CachedExecutionPlan(
            plan_id=plan_id,
            intent_query=intent_query,
            plan_steps=plan_steps,
            route_destination=route_destination,
            corpus_hash=active_corpus_hash,
            model_profile=model_profile,
            created_at=now,
            ttl_seconds=self.ttl_seconds,
            f1_score=f1_score,
            metadata=metadata
        )

        # Store in LRU
        if len(self.lru_cache) >= self.max_lru_items:
            self.lru_cache.popitem(last=False)
            self.stats["evictions"] += 1
        self.lru_cache[plan_id] = plan

        # Store in SQLite
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO plan_cache
                (plan_id, intent_query, plan_steps_json, route_destination, corpus_hash, model_profile, created_at, ttl_seconds, f1_score, metadata_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                plan.plan_id,
                plan.intent_query,
                json.dumps(plan.plan_steps),
                plan.route_destination,
                plan.corpus_hash,
                plan.model_profile,
                plan.created_at,
                plan.ttl_seconds,
                plan.f1_score,
                json.dumps(plan.metadata)
            ))
            conn.commit()

        return plan

    def lookup_plan(
        self,
        query: str,
        corpus_hash: Optional[str] = None,
        model_profile: str = "default",
        current_time: Optional[float] = None
    ) -> Tuple[Optional[CachedExecutionPlan], float]:
        """
        Looks up a plan via exact hash or semantic similarity (>= threshold).
        Returns (plan, similarity_score).
        """
        active_corpus = corpus_hash or self.current_corpus_hash
        now = current_time if current_time is not None else time.time()

        # Step 1: Check memory LRU for exact match
        exact_id = self._generate_plan_id(query, active_corpus, model_profile)
        if exact_id in self.lru_cache:
            candidate = self.lru_cache[exact_id]
            if candidate.is_expired(now):
                del self.lru_cache[exact_id]
                self.stats["stale_invalidations"] += 1
            elif candidate.corpus_hash != active_corpus and active_corpus:
                del self.lru_cache[exact_id]
                self.stats["stale_invalidations"] += 1
            else:
                self.lru_cache.move_to_end(exact_id)
                self.stats["hits"] += 1
                return candidate, 1.0

        # Step 2: Search memory and SQLite candidates for semantic match
        candidates: List[CachedExecutionPlan] = list(self.lru_cache.values())

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT plan_id, intent_query, plan_steps_json, route_destination, corpus_hash, model_profile, created_at, ttl_seconds, f1_score, metadata_json
                FROM plan_cache
                WHERE model_profile = ?
            """, (model_profile,))
            rows = cursor.fetchall()
            for r in rows:
                plan = CachedExecutionPlan(
                    plan_id=r[0],
                    intent_query=r[1],
                    plan_steps=json.loads(r[2]),
                    route_destination=r[3],
                    corpus_hash=r[4],
                    model_profile=r[5],
                    created_at=r[6],
                    ttl_seconds=r[7],
                    f1_score=r[8],
                    metadata=json.loads(r[9]) if r[9] else {}
                )
                if not any(c.plan_id == plan.plan_id for c in candidates):
                    candidates.append(plan)

        best_plan: Optional[CachedExecutionPlan] = None
        best_score = 0.0

        for cand in candidates:
            # Check expiration & corpus validity
            if cand.is_expired(now):
                self.stats["stale_invalidations"] += 1
                continue
            if active_corpus and cand.corpus_hash != active_corpus:
                self.stats["stale_invalidations"] += 1
                continue

            score = compute_text_similarity(query, cand.intent_query)
            if score > best_score:
                best_score = score
                best_plan = cand

        if best_plan and best_score >= self.similarity_threshold:
            self.stats["hits"] += 1
            # Promote to LRU
            self.lru_cache[best_plan.plan_id] = best_plan
            return best_plan, best_score

        self.stats["misses"] += 1
        return None, best_score

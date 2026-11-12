"""
Modular RAG Pipeline Coordinator for HALO RAG Studio.

Integrates:
  1. Ingestion (Allowlist validated against 15 source documents)
  2. Section-Aware Chunking
  3. Semantic Routing
  4. Hybrid BM25 / Dense Retrieval
  5. Grounded Citation Generation
  6. RAGAS 4-Metric Evaluation
"""

import os
from typing import Any, Dict, List, Optional

from src.rag.chunking import ChunkingEngine, DocumentChunk
from src.rag.citation_engine import CitationEngine
from src.rag.hybrid_retriever import HybridRetriever, ScoredChunk
from src.rag.ingestion import IngestionEngine
from src.rag.metrics import RAGEvalScores, RAGMetricsEvaluator
from src.rag.semantic_router import RouteResult, SemanticRouter


class ModularRAGPipeline:
    """
    Coordinates the 5-stage modular RAG lifecycle.
    """

    def __init__(
        self,
        corpus_dir: str = ".",
        manifest_path: str = "data/corpus_baseline_hashes.sha256",
        composite_quality_gate: float = 0.80,
        top_k: int = 4
    ):
        self.corpus_dir = corpus_dir
        self.manifest_path = manifest_path
        self.composite_quality_gate = composite_quality_gate
        self.top_k = top_k

        self.ingestion = IngestionEngine(corpus_dir=corpus_dir, manifest_path=manifest_path)
        self.chunking = ChunkingEngine()
        self.router = SemanticRouter()
        self.citation_engine = CitationEngine()
        self.evaluator = RAGMetricsEvaluator(composite_threshold=composite_quality_gate)

        # Index state
        self.documents = []
        self.chunks: List[DocumentChunk] = []
        self.retriever: Optional[HybridRetriever] = None
        self._initialize_index()

    def _initialize_index(self) -> None:
        """Ingests and chunks all verified notebook sources."""
        self.documents = self.ingestion.ingest_all()
        self.chunks = self.chunking.chunk_all(self.documents)
        self.retriever = HybridRetriever(self.chunks)

    def execute_query(
        self,
        query: str,
        plan_steps: Optional[List[str]] = None,
        enforce_routing: bool = True
    ) -> Dict[str, Any]:
        """
        Executes modular RAG pipeline for a given query.
        """
        if not self.retriever:
            raise RuntimeError("RAG index is not initialized")

        # 1. Semantic Routing
        route = self.router.route_query(query)
        doc_filter = route.target_doc_ids if (enforce_routing and route.confidence >= 0.50) else None

        # 2. Hybrid Retrieval
        scored_chunks = self.retriever.retrieve(
            query=query,
            top_k=self.top_k,
            doc_filter=doc_filter
        )

        # If filtered search returned zero results, retry across the entire corpus
        if not scored_chunks and doc_filter is not None:
            scored_chunks = self.retriever.retrieve(
                query=query,
                top_k=self.top_k,
                doc_filter=None
            )

        # 3. Grounded Citation Generation
        grounded_data = self.citation_engine.format_grounded_response(
            query=query,
            scored_chunks=scored_chunks
        )

        # 4. Evaluation
        retrieved_contexts = [sc.chunk.content for sc in scored_chunks]
        eval_scores = self.evaluator.evaluate(
            query=query,
            retrieved_contexts=retrieved_contexts,
            generated_answer=grounded_data["response"]
        )

        return {
            "query": query,
            "response": grounded_data["response"],
            "grounded": grounded_data["grounded"],
            "citations": grounded_data["citations"],
            "route": route.to_dict(),
            "evaluation": eval_scores.to_dict(),
            "destination": f"notebooks_{'_'.join(route.target_doc_ids)}"
        }

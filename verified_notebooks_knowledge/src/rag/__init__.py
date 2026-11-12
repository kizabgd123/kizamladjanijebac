"""HALO RAG Studio Modular RAG Package."""
from src.rag.chunking import ChunkingEngine, DocumentChunk
from src.rag.citation_engine import CitationEngine, GroundedCitation
from src.rag.hybrid_retriever import BM25Retriever, DenseSimilarityRetriever, HybridRetriever, ScoredChunk
from src.rag.ingestion import DocumentMetadata, IngestedDocument, IngestionEngine
from src.rag.metrics import RAGEvalScores, RAGMetricsEvaluator
from src.rag.pipeline import ModularRAGPipeline
from src.rag.semantic_router import RouteResult, SemanticRouter

__all__ = [
    "ChunkingEngine",
    "DocumentChunk",
    "CitationEngine",
    "GroundedCitation",
    "BM25Retriever",
    "DenseSimilarityRetriever",
    "HybridRetriever",
    "ScoredChunk",
    "DocumentMetadata",
    "IngestedDocument",
    "IngestionEngine",
    "RAGEvalScores",
    "RAGMetricsEvaluator",
    "ModularRAGPipeline",
    "RouteResult",
    "SemanticRouter",
]

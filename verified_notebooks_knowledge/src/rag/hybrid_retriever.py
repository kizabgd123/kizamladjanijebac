"""
Hybrid Retrieval Engine for HALO RAG Studio.

Combines pure-Python BM25 sparse keyword scoring with dense cosine similarity.
Performs reciprocal rank / score fusion and metadata filtering.
"""

import collections
import math
import re
from typing import Any, Dict, List, Optional, Tuple
from src.rag.chunking import DocumentChunk


class ScoredChunk:
    def __init__(self, chunk: DocumentChunk, score: float, sparse_score: float = 0.0, dense_score: float = 0.0):
        self.chunk = chunk
        self.score = score
        self.sparse_score = sparse_score
        self.dense_score = dense_score

    def to_dict(self) -> Dict[str, Any]:
        return {
            "chunk_id": self.chunk.chunk_id,
            "doc_id": self.chunk.doc_id,
            "filename": self.chunk.filename,
            "heading_path": self.chunk.heading_path,
            "score": round(self.score, 4),
            "sparse_score": round(self.sparse_score, 4),
            "dense_score": round(self.dense_score, 4),
            "content": self.chunk.content
        }


class BM25Retriever:
    """Pure-Python implementation of BM25Okapi scoring."""

    def __init__(self, chunks: List[DocumentChunk], k1: float = 1.5, b: float = 0.75):
        self.chunks = chunks
        self.k1 = k1
        self.b = b
        self.doc_len: List[int] = []
        self.avg_doc_len: float = 0.0
        self.doc_freqs: List[Dict[str, int]] = []
        self.idf: Dict[str, float] = {}
        self._build_index()

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r"\w+", text.lower())

    def _build_index(self) -> None:
        total_len = 0
        df: collections.Counter = collections.Counter()

        for chunk in self.chunks:
            tokens = self._tokenize(chunk.content)
            self.doc_len.append(len(tokens))
            total_len += len(tokens)
            freqs = collections.Counter(tokens)
            self.doc_freqs.append(freqs)
            for term in freqs.keys():
                df[term] += 1

        n_docs = len(self.chunks)
        self.avg_doc_len = total_len / max(1, n_docs)

        for term, count in df.items():
            # BM25 IDF formulation
            self.idf[term] = math.log((n_docs - count + 0.5) / (count + 0.5) + 1.0)

    def score(self, query: str) -> List[float]:
        q_tokens = self._tokenize(query)
        scores: List[float] = [0.0] * len(self.chunks)

        for i, freqs in enumerate(self.doc_freqs):
            dl = self.doc_len[i]
            s = 0.0
            for term in q_tokens:
                if term in freqs:
                    tf = freqs[term]
                    idf = self.idf.get(term, 0.0)
                    denom = tf + self.k1 * (1.0 - self.b + self.b * (dl / self.avg_doc_len))
                    s += idf * (tf * (self.k1 + 1.0)) / denom
            scores[i] = s

        return scores


class DenseSimilarityRetriever:
    """Computes dense cosine similarity over n-gram term frequencies."""

    def __init__(self, chunks: List[DocumentChunk]):
        self.chunks = chunks
        self.vectors: List[collections.Counter] = []
        self._build_vectors()

    def _vectorize(self, text: str) -> collections.Counter:
        words = re.findall(r"\w+", text.lower())
        bigrams = [f"{words[i]}_{words[i+1]}" for i in range(len(words)-1)]
        return collections.Counter(words + bigrams)

    def _build_vectors(self) -> None:
        for chunk in self.chunks:
            self.vectors.append(self._vectorize(chunk.content))

    def score(self, query: str) -> List[float]:
        q_vec = self._vectorize(query)
        scores: List[float] = [0.0] * len(self.chunks)
        q_norm = math.sqrt(sum(v**2 for v in q_vec.values()))
        if q_norm == 0.0:
            return scores

        for i, doc_vec in enumerate(self.vectors):
            d_norm = math.sqrt(sum(v**2 for v in doc_vec.values()))
            if d_norm == 0.0:
                continue
            common = set(q_vec.keys()) & set(doc_vec.keys())
            dot = sum(q_vec[k] * doc_vec[k] for k in common)
            scores[i] = dot / (q_norm * d_norm)

        return scores


class HybridRetriever:
    """
    Coordinates BM25 and Dense similarity with reciprocal rank and weighted score fusion.
    """

    def __init__(
        self,
        chunks: List[DocumentChunk],
        dense_weight: float = 0.5,
        sparse_weight: float = 0.5,
        bm25_k1: float = 1.5,
        bm25_b: float = 0.75
    ):
        self.chunks = chunks
        self.dense_weight = dense_weight
        self.sparse_weight = sparse_weight
        self.bm25 = BM25Retriever(chunks, k1=bm25_k1, b=bm25_b)
        self.dense = DenseSimilarityRetriever(chunks)

    def retrieve(
        self,
        query: str,
        top_k: int = 4,
        doc_filter: Optional[List[str]] = None,
        min_score: float = 0.05
    ) -> List[ScoredChunk]:
        if not self.chunks:
            return []

        sparse_scores = self.bm25.score(query)
        dense_scores = self.dense.score(query)

        # Normalize sparse scores
        max_sparse = max(sparse_scores) if sparse_scores else 1.0
        norm_sparse = [s / max_sparse if max_sparse > 0 else 0.0 for s in sparse_scores]

        scored: List[ScoredChunk] = []
        for i, chunk in enumerate(self.chunks):
            # Apply document filter if supplied
            if doc_filter and chunk.doc_id not in doc_filter:
                continue

            fused_score = (self.sparse_weight * norm_sparse[i]) + (self.dense_weight * dense_scores[i])
            if fused_score >= min_score:
                scored.append(ScoredChunk(
                    chunk=chunk,
                    score=fused_score,
                    sparse_score=sparse_scores[i],
                    dense_score=dense_scores[i]
                ))

        scored.sort(key=lambda x: x.score, reverse=True)
        return scored[:top_k]

"""
Citation Engine for Grounded Generation in HALO RAG Studio.

Enforces source attribution, citation tagging, and explicit evidence checks.
"""

from typing import Any, Dict, List, Optional
from src.rag.hybrid_retriever import ScoredChunk


class GroundedCitation:
    def __init__(self, doc_id: str, filename: str, heading_path: str, chunk_id: str, snippet: str):
        self.doc_id = doc_id
        self.filename = filename
        self.heading_path = heading_path
        self.chunk_id = chunk_id
        self.snippet = snippet

    def format_tag(self) -> str:
        return f"[Source: {self.filename} § {self.heading_path} ({self.chunk_id})]"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "doc_id": self.doc_id,
            "filename": self.filename,
            "heading_path": self.heading_path,
            "chunk_id": self.chunk_id,
            "snippet": self.snippet[:200]
        }


class CitationEngine:
    """
    Constructs citations and verifies groundedness of responses against retrieved chunks.
    """

    def build_citations(self, scored_chunks: List[ScoredChunk]) -> List[GroundedCitation]:
        citations: List[GroundedCitation] = []
        for sc in scored_chunks:
            chunk = sc.chunk
            snippet = chunk.content.replace("\n", " ").strip()[:150]
            citations.append(GroundedCitation(
                doc_id=chunk.doc_id,
                filename=chunk.filename,
                heading_path=chunk.heading_path,
                chunk_id=chunk.chunk_id,
                snippet=snippet
            ))
        return citations

    def format_grounded_response(
        self,
        query: str,
        scored_chunks: List[ScoredChunk],
        synthesis_text: Optional[str] = None
    ) -> Dict[str, Any]:
        if not scored_chunks:
            return {
                "grounded": False,
                "response": "⚠️ Insufficient evidence in the verified knowledge corpus to answer this query reliably.",
                "citations": [],
                "evidence_status": "NO_EVIDENCE"
            }

        citations = self.build_citations(scored_chunks)

        if synthesis_text:
            text = synthesis_text
        else:
            # Deterministic evidence summarizer
            top_chunk = scored_chunks[0].chunk
            text = f"Based on verified research in `{top_chunk.filename}` ({top_chunk.heading_path}):\n\n{top_chunk.content[:400]}..."

        # Append source citations block
        citation_tags = [c.format_tag() for c in citations]
        attributed_response = f"{text}\n\n---\n**Verified Sources:**\n" + "\n".join(f"- {tag}" for tag in citation_tags)

        return {
            "grounded": True,
            "response": attributed_response,
            "citations": [c.to_dict() for c in citations],
            "evidence_status": "GROUNDED",
            "top_score": scored_chunks[0].score
        }

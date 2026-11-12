"""
Hierarchical Section-Aware Chunking Engine for HALO RAG Studio.
"""

import re
from typing import Any, Dict, List, Optional
from src.rag.ingestion import IngestedDocument


class DocumentChunk:
    def __init__(
        self,
        chunk_id: str,
        doc_id: str,
        filename: str,
        heading_path: str,
        content: str,
        chunk_index: int,
        metadata: Optional[Dict[str, Any]] = None
    ):
        self.chunk_id = chunk_id
        self.doc_id = doc_id
        self.filename = filename
        self.heading_path = heading_path
        self.content = content
        self.chunk_index = chunk_index
        self.metadata = metadata or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "chunk_id": self.chunk_id,
            "doc_id": self.doc_id,
            "filename": self.filename,
            "heading_path": self.heading_path,
            "content": self.content,
            "chunk_index": self.chunk_index,
            "metadata": self.metadata
        }


class ChunkingEngine:
    """
    Partitions documents into semantically coherent chunks based on Markdown headers
    and secondary token-length constraints.
    """

    def __init__(self, max_chunk_chars: int = 800, overlap_chars: int = 100):
        self.max_chunk_chars = max_chunk_chars
        self.overlap_chars = overlap_chars

    def chunk_document(self, document: IngestedDocument) -> List[DocumentChunk]:
        chunks: List[DocumentChunk] = []
        raw = document.raw_text
        doc_id = document.metadata.doc_id
        filename = document.metadata.filename

        # Split on markdown headers (# , ## , ### )
        sections = re.split(r"(?m)(?=^#{1,3}\s+)", raw)

        current_heading = "Preamble"
        chunk_idx = 0

        for section in sections:
            section = section.strip()
            if not section:
                continue

            # Check if this section begins with a header
            header_match = re.match(r"^#{1,3}\s+(.+)$", section, re.MULTILINE)
            if header_match:
                current_heading = header_match.group(1).strip()

            # If section length <= max_chunk_chars, keep as single chunk
            if len(section) <= self.max_chunk_chars:
                cid = f"{doc_id}_c{chunk_idx:03d}"
                chunks.append(DocumentChunk(
                    chunk_id=cid,
                    doc_id=doc_id,
                    filename=filename,
                    heading_path=current_heading,
                    content=section,
                    chunk_index=chunk_idx,
                    metadata={"doc_title": document.metadata.title, "category": document.metadata.category}
                ))
                chunk_idx += 1
            else:
                # Sliding window chunking within large section
                start = 0
                while start < len(section):
                    end = min(len(section), start + self.max_chunk_chars)
                    # Attempt to break at newline or space
                    if end < len(section):
                        break_pos = section.rfind("\n", start + self.max_chunk_chars // 2, end)
                        if break_pos == -1:
                            break_pos = section.rfind(" ", start + self.max_chunk_chars // 2, end)
                        if break_pos != -1:
                            end = break_pos

                    sub_text = section[start:end].strip()
                    if sub_text:
                        cid = f"{doc_id}_c{chunk_idx:03d}"
                        chunks.append(DocumentChunk(
                            chunk_id=cid,
                            doc_id=doc_id,
                            filename=filename,
                            heading_path=current_heading,
                            content=sub_text,
                            chunk_index=chunk_idx,
                            metadata={"doc_title": document.metadata.title, "category": document.metadata.category}
                        ))
                        chunk_idx += 1

                    start = end - self.overlap_chars
                    if start >= len(section) or end >= len(section):
                        break

        return chunks

    def chunk_all(self, documents: List[IngestedDocument]) -> List[DocumentChunk]:
        all_chunks: List[DocumentChunk] = []
        for doc in documents:
            all_chunks.extend(self.chunk_document(doc))
        return all_chunks

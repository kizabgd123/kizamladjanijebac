"""Unit tests for Modular RAG Pipeline retrieval and Grounded Citation attribution."""

import os
import pytest
from src.rag.pipeline import ModularRAGPipeline
from src.rag.citation_engine import CitationEngine, GroundedCitation
from src.rag.hybrid_retriever import ScoredChunk


@pytest.fixture(scope="module")
def pipeline():
    return ModularRAGPipeline(corpus_dir=".", manifest_path="data/corpus_baseline_hashes.sha256")


def test_pipeline_indexed_all_15_documents(pipeline):
    # Verify exactly 15 source documents indexed
    assert len(pipeline.documents) == 15
    assert len(pipeline.chunks) > 15
    filenames = {d.filename for d in pipeline.documents}
    assert "01_Vas_Mozak_Ko_Je_U_Kontroli.md" in filenames
    assert "05_CodyMaster_Brain_Deterministic_RAG.md" in filenames
    assert "15_Strategic_Communication_and_Self_Positioning.md" in filenames


def test_actual_retrieval_and_citation_pointers(pipeline):
    # Query specific to 05_CodyMaster
    result = pipeline.execute_query("CodyMaster deterministicki RAG")
    assert result["grounded"] is True
    assert len(result["citations"]) > 0

    # Ensure citations point to original markdown documents
    first_citation = result["citations"][0]
    assert first_citation["filename"].endswith(".md")
    assert os.path.exists(first_citation["filename"])
    assert len(first_citation["heading_path"]) > 0
    assert len(first_citation["snippet"]) > 0


def test_citation_formatting():
    engine = CitationEngine()
    empty_res = engine.format_grounded_response(query="Nepoznato", scored_chunks=[])
    assert empty_res["grounded"] is False
    assert empty_res["evidence_status"] == "NO_EVIDENCE"
    assert len(empty_res["citations"]) == 0

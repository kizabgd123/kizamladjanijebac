---
name: rag-development
description: Build and refine the 5-stage modular RAG pipeline components.
---

# RAG Development Skill

## When to Activate
Activate when developing, enhancing, or debugging query rewriting, semantic routing, hybrid retrieval, or grounded citation generation.

## Required Context
- Modular RAG pipeline interfaces in `src/rag/`.
- Knowledge chunks from `corpus-ingestion`.
- Configuration settings in `config/halo.yaml`.

## Execution Steps
1. Implement query normalization and term-preserving rewriter.
2. Build semantic router to map query topics to target notebook documents.
3. Configure hybrid retriever combining BM25 keyword scoring and cosine vector similarity with rank reciprocal fusion.
4. Format grounded responses with explicit citation tags pointing to verified sources.
5. If evidence is below confidence threshold, trigger explicit insufficient-evidence fallback.

## Verification & Checks
- Run retrieval unit tests with known query-document pairs.
- Verify every citation references an actual, existing source chunk.

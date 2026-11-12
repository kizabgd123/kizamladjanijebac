---
name: corpus-ingestion
description: Ingest, parse, and chunk the verified 15-document notebook knowledge corpus with zero modification to sources.
---

# Corpus Ingestion Skill

## When to Activate
Activate when initializing the RAG index, updating chunking parameters, or validating source document integrity.

## Required Context
- Source directory with 15 verified `.md` files.
- `data/corpus_baseline_hashes.sha256` allowlist manifest.

## Execution Steps
1. Verify SHA-256 hashes of all 15 source documents against `data/corpus_baseline_hashes.sha256`.
2. Extract frontmatter (UUID, ownership, verification status, category) and hierarchical sections (`#`, `##`, `###`).
3. Partition text into semantic chunks with configurable token boundaries and overlap.
4. Attach complete provenance metadata (source document ID, heading path, chunk index).
5. Output structured chunk records ready for hybrid indexing.

## Verification & Checks
- Assert 0 modifications to source files (`git status --porcelain`).
- Confirm all 15 documents produce non-empty chunk lists.

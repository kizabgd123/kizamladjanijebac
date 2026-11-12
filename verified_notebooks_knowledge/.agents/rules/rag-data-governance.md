---
trigger: glob
globs:
  - "src/rag/**"
  - "data/**"
---

# RAG Data Governance & Corpus Invariance Rule

1. **Source Immutability:** Never modify, reformat, rename, or delete the 15 original knowledge source documents (`01_...` to `15_...`).
2. **Explicit Ingestion Allowlist:** Ingestion is restricted to files specified in `data/corpus_baseline_hashes.sha256`.
3. **No Contamination:** Never index generated documentation, logs, temporary test artifacts, or agent responses into the primary RAG index.
4. **Citation Provenance:** Every retrieved chunk must retain complete provenance: document UUID/ID, heading hierarchy, and chunk offset.

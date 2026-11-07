# Discovery Report: Agent A (Infrastructure, Ingestion & MCP Architecture)

**Agent ID:** Agent_A_Infra  
**Date:** 2026-11-06T23:29:00Z  
**Target:** `retail-product-search`  

## 1. Domain Background & Architecture Ingestion
The `retail-product-search` skill is an e-commerce semantic search and RAG engine built on Google Cloud Platform, specifically leveraging:
- **Storage & Tabular Catalog:** BigQuery dataset `retail_skill_products.products`.
- **Vector Retrieval Engine:** Gemini Enterprise Agent Platform Vector Search 2.0 collection `retail-skill-products-collection` located strictly in `us-central1`.
- **Embedding Generation:** Automated embedding pipeline using `gemini-embedding-001` managed directly by Vector Search 2.0.
- **Agent Framework:** Google Agent Development Kit (ADK) serving an interactive web UI (`.venv/bin/adk web`).

## 2. Mechanistic Insights & Ingestion Workflow
1. **Schema Validation Hierarchy:**
   - Catalog ingestion relies on `validate_schema.py` enforcing strict column tiers:
     - `Basic`: `product_id, name, price, description`.
     - `Standard`: `category, brand, image_url` + Basic.
     - `Extended`: `rating, stock, manufacturer` + Standard (Default for Quick Start).
     - `Full`: `variants, tags, specifications, reviews` + Extended.
   - *Mechanistic trap:* Unrecognized columns outside the tier schema cause immediate rejection rather than silent dropping.
2. **Two-Stage Cloud Ingestion:**
   - `ingest_bigquery.py`: Streams or loads catalog records into BigQuery table with schema type enforcement.
   - `ingest_vertex_search.py`: Points Vector Search 2.0 collection to BigQuery table. Embeddings are created automatically without local batch vectorization.
3. **Region Pinning Invariant:**
   - Vector Search 2.0 auto-embedding feature is exclusively verified in `us-central1`. Any attempt to deploy in alternative regions yields `501 MethodNotImplemented`.

## 3. Initial Hypotheses
- **HYP-A1 (MCP Isolation):** Migrating from local CLI Python scripts (`ingest_bigquery.py`, `ingest_vertex_search.py`) to official BigQuery and Gemini Enterprise Agent Platform MCP servers will eliminate venv dependency drift and Python interpreter conflicts (`ModuleNotFoundError: google.adk`).
- **HYP-A2 (Vector Search Indexing Latency Boundary):** The auto-indexing delay of Vector Search 2.0 (5-10 minutes post-ingestion) introduces a critical temporal failure mode where immediate evaluation calls falsely classify the system as having 0% recall.

## 4. Identified Risk Factors & Edge Cases
- **Newline Corruption:** If `VECTOR_SEARCH_COLLECTION` environment variable contains a trailing newline (`\n`), GCP client libraries throw `501 MethodNotImplemented` or invalid URI parsing errors.
- **Python Runtime Drift:** Host system using Python 3.9 will fail during venv creation; minimum requirement is Python 3.11+.
- **Venv Pollution / Tool Shadowing:** Running bare `adk` instead of `.venv/bin/adk` causes the agent to load against global python, rendering the app list empty (`/list-apps` returns `[]`).

## 5. Open Questions for Relay Phase
- How does the evaluation suite (`EVAL.yaml`) distinguish between an unindexed vector database vs. an agent reasoning failure?
- Can structured SQL filtering in BigQuery be hybrid-composed with Vector Search retrieval to handle hard numerical bounds (e.g. `price < 50`) without client-side LLM dropping?

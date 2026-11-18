# HALO RAG Studio — Benchmark Dataset Specification

## 1. Executive Summary & Design Protocol

The HALO RAG Evaluation Benchmark (`data/evaluation/rag_benchmark.jsonl`) comprises **30 strictly curated test cases** designed for independent, empirical verification of the HALO RAG Studio architecture.

The dataset adheres to the following core constraints:
- **Corpus Fidelity**: All factual assertions and expected evidence are drawn exclusively from the 15 SHA-256 verified source knowledge documents.
- **Full Corpus Coverage**: 100% of the 15 documents (`01` through `15`) are explicitly represented across the evaluation queries.
- **Taxonomic Coverage**: All 10 required evaluation query archetypes are represented.
- **Zero Hallucination / Target Leakage**: Expected evidence sentences are extracted directly from source headings and content.

---

## 2. Dataset Schema

Each entry in `data/evaluation/rag_benchmark.jsonl` conforms to the following JSON structure:

```json
{
  "case_id": "BM001",
  "category": "direct_factual",
  "query": "Koji su nivoi CodyMaster L0-L3 arhitekture i šta tačno obuhvata L0 nivo?",
  "expected_sources": ["05"],
  "expected_evidence": "L0 nivo predstavlja Micro operacije: samo Code + Test (cm-tdd -> cm-quality-gate)",
  "answerability": "answerable",
  "doc_refs": ["05_CodyMaster_Brain_Deterministic_RAG.md"]
}
```

### Field Definitions:
- `case_id` (str): Unique identifier (`BM001` - `BM030`).
- `category` (str): One of the 10 formal query categories.
- `query` (str): The natural language query presented to the RAG pipeline.
- `expected_sources` (List[str]): List of 2-digit doc IDs (`["01"]` .. `["15"]`) containing ground truth. Empty list `[]` for out-of-domain and adversarial queries.
- `expected_evidence` (str): Key factual proposition or expected handling behavior.
- `answerability` (str): `answerable`, `unanswerable`, or `adversarial`.
- `doc_refs` (List[str]): Filenames of relevant documents in the corpus.

---

## 3. Category Breakdown & Corpus Distribution

| Category ID | Category Name | Case Count | Case IDs | Target Documents |
|---|---|:---:|---|---|
| 1 | `direct_factual` | 4 | BM001 - BM004 | 05, 06, 10, 03 |
| 2 | `multi_document_synthesis` | 3 | BM005 - BM007 | (01, 13), (08, 14), (07, 09) |
| 3 | `paraphrased` | 3 | BM008 - BM010 | 06, 05, 01 |
| 4 | `ambiguous` | 3 | BM011 - BM013 | (03, 04, 05), (13, 14), (10, 12) |
| 5 | `out_of_domain` | 3 | BM014 - BM016 | None (Out of corpus) |
| 6 | `adversarial` | 3 | BM017 - BM019 | None (Injection / Jailbreak) |
| 7 | `technical_terminology` | 3 | BM020 - BM022 | 04, 11, 12 |
| 8 | `procedural_workflow` | 3 | BM023 - BM025 | 13, 02, 15 |
| 9 | `negative` | 3 | BM026 - BM028 | 15, 14, 09 |
| 10 | `edge_case` | 2 | BM029 - BM030 | 06 (Extremely short & Extremely long) |
| **Total** | **10 Categories** | **30 Cases** | **BM001 - BM030** | **All 15 documents represented** |

---

## 4. Source Document Mapping Matrix

| Doc ID | Source Filename | Covered by Benchmark Cases |
|---|---|---|
| `01` | `01_Vas_Mozak_Ko_Je_U_Kontroli.md` | BM005, BM010 |
| `02` | `02_AI_Native_Transformation_SEE_Digital_Engineering.md` | BM024 |
| `03` | `03_Project_OpenClaw_Sovereign_AI_OS.md` | BM004, BM011 |
| `04` | `04_Google_Antigravity_Agentic_IDE.md` | BM011, BM020 |
| `05` | `05_CodyMaster_Brain_Deterministic_RAG.md` | BM001, BM009, BM011 |
| `06` | `06_Prokrastinacija_Naucna_Analiza_TMT.md` | BM002, BM008, BM029, BM030 |
| `07` | `07_NotebookLM_Custom_Prompts_Advanced_AI.md` | BM007 |
| `08` | `08_LinkedIn_Automation_Agent_Brain_Franklin.md` | BM006 |
| `09` | `09_Gemini_3_Prompting_Rules_NotebookLM.md` | BM007, BM028 |
| `10` | `10_NLP_Silva_Metod_Neuroplasticnost.md` | BM003, BM013 |
| `11` | `11_2026_UI_Design_Principles_Spatial_Computing.md` | BM021 |
| `12` | `12_Duboko_Ucenje_i_Vestacka_Inteligencija.md` | BM013, BM022 |
| `13` | `13_Vestina_Pametnog_Odlucivanja_7_Koraka.md` | BM005, BM012, BM023 |
| `14` | `14_Strategija_Licnog_Brenda_Inbound_Funnel.md` | BM006, BM012, BM027 |
| `15` | `15_Strategic_Communication_and_Self_Positioning.md` | BM025, BM026 |

---

## 5. Evaluation Protocol

When executing the benchmark, test runners must measure:
1. **Retrieval Performance (IR Metrics)**:
   - Recall@1, Recall@3, Recall@5
   - Precision@1, Precision@3, Precision@5
   - Mean Reciprocal Rank (MRR)
   - Normalized Discounted Cumulative Gain (nDCG@K)
   - Comparison across: BM25-only, Dense-only (all-MiniLM-L6-v2), and Hybrid (0.5 BM25 + 0.5 Dense).
2. **Generation Quality**:
   - Citation validity: verifying that cited chunks exist, match source documents, and contain the asserted facts.
   - Groundedness flag: ensuring that responses are grounded in retrieved evidence.
   - Quality Gate: RAGAS 4-metric composite score ($Q_{rag} \ge 0.80$).
   - Rejection / Abstention: Verifying that out-of-domain and adversarial queries trigger `NO_EVIDENCE` or appropriate safety handling rather than hallucinations.

#!/usr/bin/env python3
"""
Empirical RAG Benchmark Runner for HALO RAG Studio.
Evaluates IR metrics (BM25, Dense, Hybrid) and RAG generation on the 30-case benchmark.
"""

import json
import math
import os
import sys
import time

sys.path.insert(0, os.path.abspath("."))

from src.rag.chunking import ChunkingEngine
from src.rag.hybrid_retriever import HybridRetriever
from src.rag.ingestion import IngestionEngine
from src.rag.pipeline import ModularRAGPipeline


def compute_ndcg_at_k(retrieved_docs, expected_docs, k=5):
    dcg = 0.0
    for i, doc_id in enumerate(retrieved_docs[:k]):
        rel = 1.0 if doc_id in expected_docs else 0.0
        dcg += rel / math.log2(i + 2)
    # Ideal DCG
    ideal_rel = sorted([1.0 if doc_id in expected_docs else 0.0 for doc_id in retrieved_docs[:k]], reverse=True)
    # Or maximum possible relevant docs in top k
    max_possible = min(len(expected_docs), k)
    idcg = sum(1.0 / math.log2(i + 2) for i in range(max_possible))
    if idcg == 0.0:
        return 0.0
    return dcg / idcg


def evaluate_retriever_mode(retriever, cases, top_k=5):
    results = []
    for c in cases:
        if c["answerability"] != "answerable":
            continue
        expected = set(c["expected_sources"])
        scored = retriever.retrieve(c["query"], top_k=top_k)
        retrieved_doc_ids = [sc.chunk.doc_id for sc in scored]

        # Recall@K
        r1 = 1.0 if any(d in expected for d in retrieved_doc_ids[:1]) else 0.0
        r3 = 1.0 if any(d in expected for d in retrieved_doc_ids[:3]) else 0.0
        r5 = 1.0 if any(d in expected for d in retrieved_doc_ids[:5]) else 0.0

        # Precision@K
        p1 = len([d for d in retrieved_doc_ids[:1] if d in expected]) / 1.0 if retrieved_doc_ids else 0.0
        p3 = len([d for d in retrieved_doc_ids[:3] if d in expected]) / 3.0 if len(retrieved_doc_ids) >= 3 else 0.0
        p5 = len([d for d in retrieved_doc_ids[:5] if d in expected]) / 5.0 if len(retrieved_doc_ids) >= 5 else 0.0

        # RR
        rr = 0.0
        for rank, d in enumerate(retrieved_doc_ids, start=1):
            if d in expected:
                rr = 1.0 / rank
                break

        # nDCG@5
        ndcg5 = compute_ndcg_at_k(retrieved_doc_ids, expected, k=5)

        results.append({
            "case_id": c["case_id"],
            "category": c["category"],
            "recall@1": r1,
            "recall@3": r3,
            "recall@5": r5,
            "precision@1": p1,
            "precision@3": p3,
            "precision@5": p5,
            "rr": rr,
            "ndcg@5": ndcg5
        })
    return results


def main():
    print("Loading benchmark cases...")
    with open("data/evaluation/rag_benchmark.jsonl", "r", encoding="utf-8") as f:
        cases = [json.loads(line) for line in f]

    pipeline = ModularRAGPipeline()
    chunks = pipeline.chunks

    # Initializing retrievers
    bm25_retriever = HybridRetriever(chunks, dense_weight=0.0, sparse_weight=1.0)
    dense_retriever = HybridRetriever(chunks, dense_weight=1.0, sparse_weight=0.0)
    hybrid_retriever = pipeline.retriever

    print("\n--- Evaluating Retrieval Modes on Answerable Cases (24 cases) ---")
    bm25_res = evaluate_retriever_mode(bm25_retriever, cases)
    dense_res = evaluate_retriever_mode(dense_retriever, cases)
    hybrid_res = evaluate_retriever_mode(hybrid_retriever, cases)

    def avg(lst, key):
        return sum(x[key] for x in lst) / len(lst) if lst else 0.0

    modes = {
        "BM25 Only": bm25_res,
        "Dense Only": dense_res,
        "Hybrid (50/50)": hybrid_res
    }

    summary_lines = []
    summary_lines.append("=== RETRIEVAL IR BENCHMARK SUMMARY (N=24 Answerable Cases) ===")
    summary_lines.append(f"{'Mode':<18} | {'Recall@1':<9} | {'Recall@3':<9} | {'Recall@5':<9} | {'Prec@3':<8} | {'MRR':<8} | {'nDCG@5':<8}")
    summary_lines.append("-" * 80)
    for name, res in modes.items():
        summary_lines.append(
            f"{name:<18} | {avg(res, 'recall@1'):<9.4f} | {avg(res, 'recall@3'):<9.4f} | {avg(res, 'recall@5'):<9.4f} | "
            f"{avg(res, 'precision@3'):<8.4f} | {avg(res, 'rr'):<8.4f} | {avg(res, 'ndcg@5'):<8.4f}"
        )

    # Category breakdown for Hybrid
    summary_lines.append("\n=== HYBRID RETRIEVAL METRICS BY CATEGORY ===")
    summary_lines.append(f"{'Category':<26} | {'N':<3} | {'R@1':<6} | {'R@3':<6} | {'R@5':<6} | {'MRR':<6} | {'nDCG@5':<6}")
    summary_lines.append("-" * 75)
    cat_groups = {}
    for r in hybrid_res:
        cat_groups.setdefault(r["category"], []).append(r)
    for cat, items in sorted(cat_groups.items()):
        summary_lines.append(
            f"{cat:<26} | {len(items):<3} | {avg(items, 'recall@1'):<6.3f} | {avg(items, 'recall@3'):<6.3f} | "
            f"{avg(items, 'recall@5'):<6.3f} | {avg(items, 'rr'):<6.3f} | {avg(items, 'ndcg@5'):<6.3f}"
        )

    print("\n".join(summary_lines))

    print("\n--- Evaluating Modular RAG Pipeline Generation Across All 30 Cases ---")
    gen_results = []
    for c in cases:
        t0 = time.perf_counter()
        exec_res = pipeline.execute_query(c["query"])
        elapsed_ms = (time.perf_counter() - t0) * 1000

        expected = set(c["expected_sources"])
        cited_docs = [cit["doc_id"] for cit in exec_res["citations"]]
        
        # Citation precision
        if expected:
            hit = any(d in expected for d in cited_docs)
            correct_cits = [d for d in cited_docs if d in expected]
            cit_prec = len(correct_cits) / len(cited_docs) if cited_docs else 0.0
        else:
            hit = (len(cited_docs) == 0)
            cit_prec = 1.0 if not cited_docs else 0.0

        gen_results.append({
            "case_id": c["case_id"],
            "category": c["category"],
            "query": c["query"],
            "answerability": c["answerability"],
            "expected_sources": c["expected_sources"],
            "cited_docs": cited_docs,
            "grounded": exec_res["grounded"],
            "citation_hit": hit,
            "citation_precision": round(cit_prec, 4),
            "route_category": exec_res["route"]["category"],
            "route_confidence": exec_res["route"]["confidence"],
            "evaluation": exec_res["evaluation"],
            "elapsed_ms": round(elapsed_ms, 2)
        })

    # Save full JSON
    all_artifacts = {
        "benchmark_timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "total_cases": len(cases),
        "retrieval_modes": {
            "bm25": bm25_res,
            "dense": dense_res,
            "hybrid": hybrid_res
        },
        "pipeline_generation": gen_results
    }
    with open("artifacts/acceptance/rag_benchmark_results.json", "w", encoding="utf-8") as f:
        json.dump(all_artifacts, f, indent=2, ensure_ascii=False)

    # Pipeline generation summary
    ans_gen = [g for g in gen_results if g["answerability"] == "answerable"]
    unans_gen = [g for g in gen_results if g["answerability"] != "answerable"]

    summary_lines.append("\n=== PIPELINE GENERATION EVALUATION ===")
    summary_lines.append(f"Answerable Cases Evaluated: {len(ans_gen)}")
    summary_lines.append(f"  Average Composite Score (Q_rag): {sum(g['evaluation']['composite_score'] for g in ans_gen)/len(ans_gen):.4f} (Gate: >= 0.80)")
    summary_lines.append(f"  Cases Passing Composite Gate (>=0.80): {sum(1 for g in ans_gen if g['evaluation']['passed_gate'])} / {len(ans_gen)} ({sum(1 for g in ans_gen if g['evaluation']['passed_gate'])/len(ans_gen)*100:.1f}%)")
    summary_lines.append(f"  Average Answer Faithfulness: {sum(g['evaluation']['answer_faithfulness'] for g in ans_gen)/len(ans_gen):.4f}")
    summary_lines.append(f"  Average Context Relevance: {sum(g['evaluation']['context_relevance'] for g in ans_gen)/len(ans_gen):.4f}")
    summary_lines.append(f"  Average Answer Relevance: {sum(g['evaluation']['answer_relevance'] for g in ans_gen)/len(ans_gen):.4f}")
    summary_lines.append(f"  Average Noise Robustness: {sum(g['evaluation']['noise_robustness'] for g in ans_gen)/len(ans_gen):.4f}")
    summary_lines.append(f"  Citation Hit Rate (Expected Doc Cited): {sum(1 for g in ans_gen if g['citation_hit'])} / {len(ans_gen)} ({sum(1 for g in ans_gen if g['citation_hit'])/len(ans_gen)*100:.1f}%)")
    summary_lines.append(f"  Average Pipeline Latency: {sum(g['elapsed_ms'] for g in ans_gen)/len(ans_gen):.2f} ms")

    summary_lines.append(f"\nUnanswerable & Adversarial Cases Evaluated: {len(unans_gen)}")
    summary_lines.append(f"  Cases Triggering Rejection/NO_EVIDENCE: {sum(1 for g in unans_gen if not g['grounded'])} / {len(unans_gen)} ({sum(1 for g in unans_gen if not g['grounded'])/len(unans_gen)*100:.1f}%)")
    summary_lines.append(f"  Cases Incorrectly Grounded (Hallucinated Evidence): {sum(1 for g in unans_gen if g['grounded'])} / {len(unans_gen)} ({sum(1 for g in unans_gen if g['grounded'])/len(unans_gen)*100:.1f}%)")

    with open("artifacts/acceptance/rag_benchmark_summary.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(summary_lines) + "\n")

    print("\nSaved artifacts to:")
    print("  - artifacts/acceptance/rag_benchmark_results.json")
    print("  - artifacts/acceptance/rag_benchmark_summary.txt")

if __name__ == "__main__":
    main()

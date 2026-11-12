#!/usr/bin/env python3
"""
Corpus Integrity Verification Script for HALO RAG Studio.
Verifies all 15 source documents against data/corpus_baseline_hashes.sha256.
"""

import sys
import os

# Ensure current working directory is in sys.path
sys.path.insert(0, os.path.abspath("."))

from src.rag.ingestion import IngestionEngine

def main():
    try:
        engine = IngestionEngine(manifest_path="data/corpus_baseline_hashes.sha256")
        results = engine.verify_corpus_integrity()
        
        all_passed = True
        print("=== HALO RAG Corpus Baseline Integrity Audit ===")
        for fname, ok in sorted(results.items()):
            status = "✅ PASSED" if ok else "❌ CORRUPTED/MISSING"
            if not ok:
                all_passed = False
            print(f"[{status}] {fname}")
            
        if all_passed:
            print("\nSUCCESS: All 15 verified notebook sources matched their baseline SHA-256 hashes bit-for-bit.")
            sys.exit(0)
        else:
            print("\nFAILURE: One or more corpus files failed integrity checks!")
            sys.exit(1)
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

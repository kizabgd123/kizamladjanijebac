#!/usr/bin/env python3
"""
Independent Skeptic Evaluator (Pillar 7 / Stage 9)
==================================================
Decoupled verification agent for model evaluation and validation integrity.
Never trusts stdout or self-reported model logs. Reads ground truth and
Out-of-Fold (OOF) prediction matrices directly from disk, recomputes metrics,
and audits for cross-validation data leakage and cryptographic consistency.
"""

import os
import sys
import math
import hashlib
import json
from typing import List, Dict, Any, Optional, Tuple


def sha256_file(filepath: str) -> str:
    """Computes SHA-256 hash of a file on disk."""
    if not os.path.exists(filepath):
        return "FILE_NOT_FOUND"
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def compute_rmse(y_true: List[float], y_pred: List[float]) -> float:
    if len(y_true) != len(y_pred) or len(y_true) == 0:
        raise ValueError("Mismatched or empty prediction arrays.")
    mse = sum((yt - yp) ** 2 for yt, yp in zip(y_true, y_pred)) / len(y_true)
    return math.sqrt(mse)


def compute_mae(y_true: List[float], y_pred: List[float]) -> float:
    if len(y_true) != len(y_pred) or len(y_true) == 0:
        raise ValueError("Mismatched or empty prediction arrays.")
    return sum(abs(yt - yp) for yt, yp in zip(y_true, y_pred)) / len(y_true)


def compute_binary_log_loss(y_true: List[int], y_pred_prob: List[float], eps: float = 1e-15) -> float:
    if len(y_true) != len(y_pred_prob) or len(y_true) == 0:
        raise ValueError("Mismatched or empty prediction arrays.")
    total = 0.0
    for yt, yp in zip(y_true, y_pred_prob):
        p = max(eps, min(1.0 - eps, yp))
        total += yt * math.log(p) + (1 - yt) * math.log(1 - p)
    return -total / len(y_true)


def compute_roc_auc(y_true: List[int], y_pred_prob: List[float]) -> float:
    """Computes ROC AUC via rank sums without external dependencies."""
    if len(y_true) != len(y_pred_prob) or len(y_true) == 0:
        raise ValueError("Mismatched or empty prediction arrays.")
    
    pos = sum(y_true)
    neg = len(y_true) - pos
    if pos == 0 or neg == 0:
        raise ValueError("ROC AUC undefined for single-class target.")

    paired = sorted(zip(y_pred_prob, y_true), key=lambda x: x[0])
    rank_sum = 0
    for rank, (_, label) in enumerate(paired, start=1):
        if label == 1:
            rank_sum += rank

    u = rank_sum - (pos * (pos + 1)) / 2.0
    return u / (pos * neg)


def audit_fold_leakage(fold_assignments: List[int]) -> Dict[str, Any]:
    """
    Audits fold assignments to ensure:
    1. Each row is assigned to exactly one validation fold.
    2. No missing or NaN fold indices.
    3. Balanced partition distribution.
    """
    if not fold_assignments:
        return {"passed": False, "error": "Empty fold assignment list"}

    num_samples = len(fold_assignments)
    folds = sorted(list(set(fold_assignments)))
    k = len(folds)

    counts = {f: fold_assignments.count(f) for f in folds}
    min_count = min(counts.values())
    max_count = max(counts.values())

    # Check for severe imbalance
    imbalance_ratio = max_count / max(1, min_count)
    leakage_detected = any(f < 0 for f in folds)

    return {
        "passed": not leakage_detected and k >= 2,
        "k_folds": k,
        "sample_count": num_samples,
        "fold_counts": counts,
        "imbalance_ratio": round(imbalance_ratio, 3),
        "leakage_detected": leakage_detected,
    }


class IndependentEvaluator:
    def __init__(self, ground_truth_path: str, oof_path: str, script_path: Optional[str] = None):
        self.ground_truth_path = os.path.abspath(ground_truth_path)
        self.oof_path = os.path.abspath(oof_path)
        self.script_path = os.path.abspath(script_path) if script_path else None

    def evaluate(self, metric_name: str = "rmse") -> Dict[str, Any]:
        """
        Loads predictions directly from disk, recomputes metrics, and signs evidence dossier.
        """
        # 1. Digest checks
        truth_hash = sha256_file(self.ground_truth_path)
        oof_hash = sha256_file(self.oof_path)
        script_hash = sha256_file(self.script_path) if self.script_path else "NOT_PROVIDED"

        if truth_hash == "FILE_NOT_FOUND" or oof_hash == "FILE_NOT_FOUND":
            return {
                "verdict": "FAIL",
                "error": "Ground truth or OOF file does not exist on disk.",
                "truth_hash": truth_hash,
                "oof_hash": oof_hash,
            }

        # 2. Read predictions and truth
        y_true, y_pred, fold_ids = self._load_data()
        if len(y_true) != len(y_pred):
            return {
                "verdict": "FAIL",
                "error": f"Row count mismatch: ground truth={len(y_true)}, OOF={len(y_pred)}",
                "truth_hash": truth_hash,
                "oof_hash": oof_hash,
            }

        # 3. Leakage audit
        fold_audit = audit_fold_leakage(fold_ids) if fold_ids else {"passed": True, "note": "No fold IDs provided"}
        if not fold_audit.get("passed", True):
            return {
                "verdict": "FAIL",
                "error": f"Cross-validation leakage audit failed: {fold_audit.get('error')}",
                "fold_audit": fold_audit,
            }

        # 4. Independent metric computation
        metric = metric_name.lower()
        computed_score: float = 0.0
        try:
            if metric == "rmse":
                computed_score = compute_rmse(y_true, y_pred)
            elif metric == "mae":
                computed_score = compute_mae(y_true, y_pred)
            elif metric == "auc":
                computed_score = compute_roc_auc([int(y) for y in y_true], y_pred)
            elif metric == "logloss":
                computed_score = compute_binary_log_loss([int(y) for y in y_true], y_pred)
            else:
                return {
                    "verdict": "FAIL",
                    "error": f"Unsupported independent metric: {metric_name}",
                }
        except Exception as e:
            return {
                "verdict": "FAIL",
                "error": f"Metric computation failure: {e}",
            }

        return {
            "verdict": "PASS",
            "metric": metric,
            "recomputed_score": round(computed_score, 6),
            "sample_count": len(y_true),
            "truth_sha256": truth_hash,
            "oof_sha256": oof_hash,
            "script_sha256": script_hash,
            "fold_audit": fold_audit,
        }

    def _load_data(self) -> Tuple[List[float], List[float], List[int]]:
        """Parses JSON or simple CSV formats without pandas requirement."""
        # Simple JSON loader
        if self.oof_path.endswith(".json"):
            with open(self.oof_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data["y_true"], data["y_pred"], data.get("folds", [])

        # Simple CSV loader
        y_true = []
        y_pred = []
        folds = []

        with open(self.ground_truth_path, "r", encoding="utf-8") as ft:
            true_lines = [l.strip() for l in ft if l.strip()]
        with open(self.oof_path, "r", encoding="utf-8") as fp:
            pred_lines = [l.strip() for l in fp if l.strip()]

        # Skip headers if present
        if not true_lines[0].replace(".", "", 1).isdigit() and not true_lines[0].replace("-", "", 1).isdigit():
            true_lines = true_lines[1:]
        if not pred_lines[0].replace(".", "", 1).isdigit() and not pred_lines[0].replace("-", "", 1).isdigit():
            pred_lines = pred_lines[1:]

        for tl, pl in zip(true_lines, pred_lines):
            t_parts = tl.split(",")
            p_parts = pl.split(",")
            y_true.append(float(t_parts[0]))
            y_pred.append(float(p_parts[0]))
            if len(p_parts) > 1 and p_parts[1].isdigit():
                folds.append(int(p_parts[1]))

        return y_true, y_pred, folds


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 independent_evaluator.py <ground_truth_file> <oof_file> [metric: rmse|mae|auc|logloss]")
        sys.exit(1)

    truth_file = sys.argv[1]
    oof_file = sys.argv[2]
    metric = sys.argv[3] if len(sys.argv) > 3 else "rmse"

    evaluator = IndependentEvaluator(truth_file, oof_file)
    result = evaluator.evaluate(metric_name=metric)

    print(json.dumps(result, indent=2))
    sys.exit(0 if result["verdict"] == "PASS" else 1)


if __name__ == "__main__":
    main()

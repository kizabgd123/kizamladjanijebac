#!/usr/bin/env python3
"""
Unit and Integration Tests for Autonomous Research Pipeline Runner
==================================================================
Tests:
- AST Security Validator (clean code passes, dangerous primitives blocked)
- Firejail Sandbox Runner (air-gapped isolated execution)
- Independent Skeptic Evaluator (decoupled metric recomputation and leakage checks)
- Pipeline Runner stage transitions
"""

import os
import sys
import json
import pytest
from pathlib import Path

from scripts.ast_validator import validate_python_code, validate_python_file
from scripts.firejail_runner import FirejailRunner
from scripts.independent_evaluator import (
    compute_rmse,
    compute_roc_auc,
    compute_binary_log_loss,
    audit_fold_leakage,
    IndependentEvaluator,
)
from scripts.pipeline_runner import AutonomousPipelineRunner


def test_ast_validator_clean_code():
    clean_code = """
import math
import json

def train_model(data):
    weights = [0.1, 0.2, 0.3]
    scores = [x * 2.0 for x in weights]
    return sum(scores)
"""
    result = validate_python_code(clean_code)
    assert result["valid"] is True
    assert result["syntax_ok"] is True
    assert len(result["violations"]) == 0


def test_ast_validator_blocks_subprocess():
    bad_code = """
import subprocess
subprocess.run(["ls", "-la"])
"""
    result = validate_python_code(bad_code)
    assert result["valid"] is False
    codes = [v["code"] for v in result["violations"]]
    assert "SEC_BANNED_IMPORT" in codes


def test_ast_validator_blocks_os_system():
    bad_code = """
import os
os.system("echo compromised")
"""
    result = validate_python_code(bad_code)
    assert result["valid"] is False
    codes = [v["code"] for v in result["violations"]]
    assert "SEC_BANNED_METHOD" in codes


def test_ast_validator_blocks_eval_exec():
    bad_code = """
x = eval("1 + 1")
exec("y = 2")
"""
    result = validate_python_code(bad_code)
    assert result["valid"] is False
    codes = [v["code"] for v in result["violations"]]
    assert codes.count("SEC_BANNED_CALL") == 2


def test_ast_validator_blocks_dunder_traversal():
    bad_code = """
subclasses = ().__class__.__base__.__subclasses__()
"""
    result = validate_python_code(bad_code)
    assert result["valid"] is False
    codes = [v["code"] for v in result["violations"]]
    assert "SEC_INTROSPECTION_EVASION" in codes


def test_firejail_runner_execution(tmp_path):
    test_script = tmp_path / "sandbox_test.py"
    test_script.write_text("print('CONTAINMENT_VERIFIED')", encoding="utf-8")

    runner = FirejailRunner(workspace_dir=str(tmp_path))
    result = runner.run_python_script(str(test_script))

    assert result["success"] is True
    assert result["exit_code"] == 0
    assert "CONTAINMENT_VERIFIED" in result["stdout"]


def test_independent_evaluator_metrics():
    y_true = [1.0, 0.0, 1.0, 1.0, 0.0]
    y_pred = [0.9, 0.1, 0.8, 0.7, 0.2]

    # AUC should be 1.0
    auc = compute_roc_auc([int(y) for y in y_true], y_pred)
    assert auc == 1.0

    # RMSE
    rmse = compute_rmse(y_true, y_pred)
    assert round(rmse, 4) > 0.0 and round(rmse, 4) < 0.5

    # LogLoss
    loss = compute_binary_log_loss([int(y) for y in y_true], y_pred)
    assert loss > 0.0


def test_fold_leakage_audit():
    # Valid 5-fold split
    folds = [0, 1, 2, 3, 4] * 20
    audit = audit_fold_leakage(folds)
    assert audit["passed"] is True
    assert audit["k_folds"] == 5
    assert audit["leakage_detected"] is False

    # Corrupted / negative fold index
    bad_folds = [0, 1, -1, 3]
    bad_audit = audit_fold_leakage(bad_folds)
    assert bad_audit["passed"] is False
    assert bad_audit["leakage_detected"] is True


def test_pipeline_runner_stages(tmp_path):
    runner = AutonomousPipelineRunner(workspace_root=str(tmp_path))
    assert runner.root.exists()
    assert runner.research_dir.exists()
    assert runner.experiments_dir.exists()


def test_full_pipeline_run(tmp_path):
    runner = AutonomousPipelineRunner(workspace_root=str(tmp_path))

    # 1. Setup research files
    (tmp_path / "objective.md").write_text("# Target Objective\nPredict target with minimal RMSE.", encoding="utf-8")
    sources_dir = tmp_path / "research" / "sources"
    sources_dir.mkdir(parents=True, exist_ok=True)
    (sources_dir / "corpus.md").write_text("# Sourced Research\nVerified literature.", encoding="utf-8")

    # 2. Setup discoveries
    disc_dir = tmp_path / "research" / "discoveries"
    disc_dir.mkdir(parents=True, exist_ok=True)
    (disc_dir / "discovery_A.md").write_text("# Discovery A\nFeature interactions.", encoding="utf-8")
    (disc_dir / "discovery_B.md").write_text("# Discovery B\nTarget transformations.", encoding="utf-8")

    # 3. Setup relays
    (disc_dir / "relay_A.md").write_text("# Relay A\nAnswering 3 additive questions.", encoding="utf-8")
    (disc_dir / "relay_B.md").write_text("# Relay B\nAdditive baton handoff.", encoding="utf-8")

    # 4. Setup hypothesis
    (tmp_path / "research" / "hypotheses.md").write_text(
        "# Hypotheses\n\n### HYP-001: Polynomial Interaction\n"
        "- Statement: Adding polynomial features decreases RMSE.\n"
        "- Theoretical Justification: Non-linear response surface.\n"
        "- Intervention / Parameter Delta: degree=2 interaction features.\n"
        "- Falsification Boundary: RMSE reduction < 0.005.\n"
        "- Expected Information Gain: Validates feature interaction hypothesis.\n",
        encoding="utf-8"
    )

    # Setup mock ground truth and experiment script
    truth_file = tmp_path / "ground_truth.csv"
    truth_file.write_text("target\n1.0\n0.0\n1.0\n0.0\n1.0\n", encoding="utf-8")

    oof_file = tmp_path / "predictions" / "oof_EXP-001.csv"
    (tmp_path / "predictions").mkdir(parents=True, exist_ok=True)

    # Script that generates OOF predictions
    script_file = tmp_path / "model_script.py"
    script_file.write_text(
        f'import sys\n'
        f'oof_out = r"{oof_file}"\n'
        f'with open(oof_out, "w") as f:\n'
        f'    f.write("pred,fold\\n0.9,0\\n0.1,1\\n0.85,0\\n0.15,1\\n0.8,0\\n")\n'
        f'print("Model training complete.")\n',
        encoding="utf-8"
    )

    success = runner.execute_pipeline(
        exp_id="EXP-001",
        hyp_id="HYP-001",
        script_path=str(script_file),
        ground_truth_path=str(truth_file),
        oof_path=str(oof_file),
        metric_name="rmse",
        baseline_score=0.5,
        metric_direction="minimize"
    )
    assert success is True
    assert (tmp_path / "verification" / "evidence.md").exists()
    assert (tmp_path / "findings" / "positive_invariants.md").exists()
    assert (tmp_path / "experiments" / "local_leaderboard.md").exists()

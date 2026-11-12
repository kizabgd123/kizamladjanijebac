"""Unit tests for bounded Monte Carlo Tree Search (MCTS) reasoner."""

import time
import pytest
from src.core.mcts import MCTSNode, MCTSReasoner, MCTSResult


def test_mcts_bounded_depth_and_simulations():
    reasoner = MCTSReasoner(rollout_depth=2, simulations=5, random_seed=42)

    def actions(state, depth):
        if depth == 0:
            return ["stepA", "stepB"]
        elif depth == 1:
            return ["substep1", "substep2"]
        return []

    def evaluate(state, traj):
        return 0.9 if "stepA" in traj else 0.3

    result = reasoner.search("RootState", actions, evaluate)
    assert isinstance(result, MCTSResult)
    assert len(result.best_trajectory) <= 2
    assert result.total_simulations == 5
    assert result.tree_size > 1
    assert result.best_value >= 0.0


def test_mcts_timeout_budget():
    # Enforce ultra-short budget of 0.001 ms to verify bounded time budget
    reasoner = MCTSReasoner(rollout_depth=5, simulations=1000, max_budget_ms=0.01)

    def actions(state, depth):
        time.sleep(0.002)
        return ["a1", "a2"]

    def evaluate(state, traj):
        return 0.5

    result = reasoner.search("Root", actions, evaluate)
    # Must terminate quickly without running all 1000 simulations
    assert result.total_simulations < 1000


def test_mcts_deterministic_seed():
    r1 = MCTSReasoner(rollout_depth=3, simulations=6, random_seed=123)
    r2 = MCTSReasoner(rollout_depth=3, simulations=6, random_seed=123)

    def actions(state, depth):
        return ["opt1", "opt2", "opt3"]

    def evaluate(state, traj):
        return 0.8 if "opt2" in traj else 0.4

    res1 = r1.search("Init", actions, evaluate)
    res2 = r2.search("Init", actions, evaluate)
    assert res1.best_trajectory == res2.best_trajectory

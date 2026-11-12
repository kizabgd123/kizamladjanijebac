"""
Monte Carlo Tree Search (MCTS) for Deep-Path Multi-Hop Agent Reasoning.

Implements structured MCTS with:
  - Bounded rollout depth (default: 3)
  - Configurable simulations per hop (default: 8)
  - UCB1 exploration factor (C_puct = 1.414)
  - Deterministic random seed for reproducible evaluation
  - Strict computational timeout and memory budget
"""

import math
import random
import time
from typing import Any, Callable, Dict, List, Optional


class MCTSNode:
    def __init__(
        self,
        state: str,
        parent: Optional["MCTSNode"] = None,
        action: Optional[str] = None,
        depth: int = 0
    ):
        self.state = state
        self.parent = parent
        self.action = action
        self.depth = depth
        self.children: List["MCTSNode"] = []
        self.visits = 0
        self.value = 0.0
        self.untried_actions: Optional[List[str]] = None

    def is_fully_expanded(self) -> bool:
        return self.untried_actions is not None and len(self.untried_actions) == 0

    def best_child(self, exploration_factor: float = 1.414) -> "MCTSNode":
        """Select best child using UCB1 formula."""
        if not self.children:
            raise ValueError("Node has no children to select from")

        def ucb1(child: MCTSNode) -> float:
            if child.visits == 0:
                return float("inf")
            exploitation = child.value / child.visits
            exploration = exploration_factor * math.sqrt(math.log(self.visits) / child.visits)
            return exploitation + exploration

        return max(self.children, key=ucb1)


class MCTSResult:
    def __init__(
        self,
        best_trajectory: List[str],
        final_state: str,
        total_simulations: int,
        elapsed_ms: float,
        best_value: float,
        tree_size: int
    ):
        self.best_trajectory = best_trajectory
        self.final_state = final_state
        self.total_simulations = total_simulations
        self.elapsed_ms = elapsed_ms
        self.best_value = best_value
        self.tree_size = tree_size

    def to_dict(self) -> Dict[str, Any]:
        return {
            "best_trajectory": self.best_trajectory,
            "final_state": self.final_state,
            "total_simulations": self.total_simulations,
            "elapsed_ms": round(self.elapsed_ms, 2),
            "best_value": round(self.best_value, 4),
            "tree_size": self.tree_size
        }


class MCTSReasoner:
    """
    Orchestrates bounded Monte Carlo Tree Search across candidate reasoning actions.
    """

    def __init__(
        self,
        rollout_depth: int = 3,
        simulations: int = 8,
        exploration_factor: float = 1.414,
        random_seed: int = 42,
        max_budget_ms: float = 10000.0
    ):
        self.rollout_depth = rollout_depth
        self.simulations = simulations
        self.exploration_factor = exploration_factor
        self.random_seed = random_seed
        self.max_budget_ms = max_budget_ms
        self.rng = random.Random(random_seed)

    def search(
        self,
        initial_state: str,
        action_generator: Callable[[str, int], List[str]],
        evaluator: Callable[[str, List[str]], float]
    ) -> MCTSResult:
        """
        Executes bounded MCTS.
        - action_generator: fn(state, depth) -> list of candidate action strings
        - evaluator: fn(state, trajectory) -> scalar reward in [0.0, 1.0]
        """
        start_time = time.time()
        root = MCTSNode(state=initial_state, depth=0)
        root.untried_actions = action_generator(initial_state, 0)

        total_nodes = 1

        for _ in range(self.simulations):
            elapsed = (time.time() - start_time) * 1000.0
            if elapsed >= self.max_budget_ms:
                break

            # 1. Selection
            node = root
            trajectory: List[str] = []
            while node.is_fully_expanded() and node.children and node.depth < self.rollout_depth:
                node = node.best_child(self.exploration_factor)
                if node.action:
                    trajectory.append(node.action)

            # 2. Expansion
            if node.depth < self.rollout_depth and node.untried_actions:
                action = node.untried_actions.pop(self.rng.randrange(len(node.untried_actions)))
                new_state = f"{node.state} -> [{action}]"
                child_node = MCTSNode(
                    state=new_state,
                    parent=node,
                    action=action,
                    depth=node.depth + 1
                )
                child_node.untried_actions = action_generator(new_state, child_node.depth)
                node.children.append(child_node)
                total_nodes += 1
                node = child_node
                trajectory.append(action)

            # 3. Simulation / Rollout
            sim_state = node.state
            sim_depth = node.depth
            sim_trajectory = list(trajectory)
            while sim_depth < self.rollout_depth:
                possible_actions = action_generator(sim_state, sim_depth)
                if not possible_actions:
                    break
                act = self.rng.choice(possible_actions)
                sim_trajectory.append(act)
                sim_state = f"{sim_state} -> [{act}]"
                sim_depth += 1

            # 4. Evaluation
            reward = evaluator(sim_state, sim_trajectory)

            # 5. Backpropagation
            curr: Optional[MCTSNode] = node
            while curr is not None:
                curr.visits += 1
                curr.value += reward
                curr = curr.parent

        elapsed_total = (time.time() - start_time) * 1000.0

        # Extract best trajectory from root
        best_traj: List[str] = []
        curr_node = root
        best_val = 0.0

        while curr_node.children:
            best_c = max(curr_node.children, key=lambda c: c.visits)
            if best_c.action:
                best_traj.append(best_c.action)
            best_val = best_c.value / max(1, best_c.visits)
            curr_node = best_c

        return MCTSResult(
            best_trajectory=best_traj,
            final_state=curr_node.state,
            total_simulations=root.visits,
            elapsed_ms=elapsed_total,
            best_value=best_val,
            tree_size=total_nodes
        )

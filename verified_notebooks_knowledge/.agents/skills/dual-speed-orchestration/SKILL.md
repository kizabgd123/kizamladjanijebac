---
name: dual-speed-orchestration
description: Operate and calibrate Option C Dual-Speed routing, AgentReuse plan caching, and ARS certainty gates.
---

# Dual-Speed Orchestration Skill

## When to Activate
Activate when configuring runtime routing between Fast-Path and Deep-Path execution channels.

## Required Context
- Hyperparameters in `config/halo.yaml`.
- Plan cache database in `data/agent_reuse_cache.db`.
- ARS certainty estimators in `src/core/ars_gate.py`.

## Execution Steps
1. Evaluate incoming user query through the AgentReuse intent classifier.
2. If intent matches a cached plan ($\sigma \ge 0.92$) and ARS Checkpoint 1 passes ($\tau_1 \ge 0.90$), execute cached plan directly via Fast-Path.
3. If intent is novel or certainty is below threshold, escalate to Deep-Path.
4. Deep-Path executes 3-tier HALO decomposition with MCTS rollouts ($D=3, N=8, C=1.414$).
5. Validate any generated code policy via AST parser before execution.
6. Record execution trajectory and cache verified plans into AgentReuse store.

## Verification & Checks
- Verify cache hit returns in $<100$ms.
- Confirm high-risk actions automatically bypass Fast-Path.

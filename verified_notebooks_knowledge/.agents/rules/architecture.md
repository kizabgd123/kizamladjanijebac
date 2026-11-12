---
trigger: always_on
---

# Architecture & Modularity Rule

1. **Option C Adherence:** All runtime components must conform to the Dual-Speed Production Engine (Fast-Path AgentReuse/ARS + Deep-Path HALO MCTS/CaP).
2. **Orchestration Separation:** Developer orchestration is handled by Antigravity IDE and `agy` CLI; application agent runtime is executed by `src/core/`.
3. **No Redundant Frameworks:** Do not install or import duplicate frameworks (ADK, LangGraph, CrewAI, AutoGen) without a formal ADR.
4. **Single Source of Truth:** Hyperparameters must be read from `config/halo.yaml` rather than hardcoded in Python modules.

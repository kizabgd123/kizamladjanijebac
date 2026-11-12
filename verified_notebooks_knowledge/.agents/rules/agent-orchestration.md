---
trigger: model_decision
description: Rules governing multi-agent delegation, role assignment, and task state tracking.
---

# Multi-Agent Orchestration & Task Boundaries Rule

1. **Role Specialization:** Assign tasks strictly to the designated agent role (e.g. QA to `qa-tester`, security to `security-auditor`).
2. **File Ownership:** No two agents may concurrently edit the same source file.
3. **Task Budget:** Adhere to the JudgeGuard limit of at most 5 concurrently active tasks in `WORK_LOG.md`.
4. **Independent Acceptance:** The Master Orchestrator must independently verify test results and reviews before merging work.

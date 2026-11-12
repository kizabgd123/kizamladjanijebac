---
trigger: always_on
---

# Evidence & Truth Rule

1. **Empirical Verification Required:** Never assert that a tool is installed, a model is accessible, an agent is active, or a test passed without inspecting live command output or file contents.
2. **Deterministic Logging:** Log all command outputs, exit codes, and diffs before declaring completion.
3. **Transparent Reporting:** If a feature, provider, or test fails, report the failure immediately with exact reproduction steps. Do not mask errors.

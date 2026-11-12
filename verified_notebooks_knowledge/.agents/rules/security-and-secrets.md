---
trigger: always_on
---

# Security & Secrets Isolation Rule

1. **Zero Secret Leakage:** Never commit API keys, tokens, passwords, or personal credentials to source code or configuration files.
2. **Environment Variable Injection:** All secrets must be referenced via environment variables (e.g. `GEMINI_API_KEY`, `OPENAI_API_KEY`).
3. **AST Policy Enforcement:** Model-generated code must pass static AST checks rejecting `Import`, `ImportFrom`, `exec`, `eval`, and private dunders before execution.
4. **No Destructive Operations:** Operations like `rm -rf /`, `sudo`, or modifying global system files without explicit authorization are strictly forbidden.

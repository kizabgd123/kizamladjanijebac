---
name: security-audit
description: Audit AST policy enforcement, secret isolation, MCP boundaries, and least-privilege configurations.
---

# Security Audit Skill

## When to Activate
Activate during security reviews, prior to deployment, or when modifying code execution layers.

## Required Context
- Code as Policies validator in `src/core/ast_sandbox.py`.
- MCP configuration in `.agents/mcp_config.json`.
- Environment credentials and `.env.example`.

## Execution Steps
1. Scan workspace for hardcoded API keys, passwords, or tokens.
2. Validate AST sandbox rules: verify rejection of `Import`, `ImportFrom`, `exec`, `eval`, dunder attributes.
3. Verify that MCP configurations restrict tool scope strictly to the project root.
4. Document the boundary: clearly distinguish static AST policy filtering from true OS-level sandbox isolation.

## Verification & Checks
- Zero secrets detected in git-tracked files.
- AST test suite blocks 100% of adversarial execution test cases.

---
name: litellm-integration
description: Configure and manage multi-model provider routing, base URLs, and environment credentials via LiteLLM.
---

# LiteLLM Integration Skill

## When to Activate
Activate when adding a new model provider, updating endpoints, or testing provider fallback.

## Required Context
- Provider registry in `providers.json`.
- Environment variables defining provider API keys.
- LiteLLM client adapters in `src/providers/`.

## Execution Steps
1. Define provider entry in `providers.json` with model names, base URLs, and environment variable names for keys.
2. Validate that no raw secrets are written into configuration files.
3. Verify connection using dry-run health checks and mock endpoints for testing.
4. Support provider profiles for Gemini, local Ollama, vLLM, and generic OpenAI-compatible gateways.

## Verification & Checks
- All mock tests pass offline without paid network requests.
- Credentials resolution pulls strictly from `os.environ`.

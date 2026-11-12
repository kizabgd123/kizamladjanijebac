# Provider Configuration Guide

**Project:** HALO RAG STUDIO  
**Status:** IMPLEMENTED  

---

## 1. Overview
HALO RAG Studio decouples agent orchestration from underlying LLM vendors using a lightweight JSON configuration registry (`providers.json`) paired with LiteLLM.

This architecture enables seamless switching between Google Gemini, local models (Ollama, vLLM, LM Studio), and OpenAI-compatible gateways without altering application code.

---

## 2. Configuration Schema (`providers.json`)
The registry defines named provider profiles:

```json
{
  "providers": {
    "gemini": {
      "provider_type": "google_genai",
      "model": "gemini-3.8-flash-high",
      "api_key_env": "GEMINI_API_KEY",
      "timeout_seconds": 30,
      "max_retries": 2,
      "capabilities": ["chat", "structured_output", "embeddings"]
    },
    "ollama": {
      "provider_type": "ollama",
      "base_url": "http://localhost:11434",
      "model": "llama3.2:latest",
      "timeout_seconds": 60,
      "max_retries": 1,
      "capabilities": ["chat", "embeddings"]
    },
    "mock": {
      "provider_type": "mock",
      "model": "deterministic-mock-v1",
      "timeout_seconds": 5,
      "max_retries": 0,
      "capabilities": ["chat", "structured_output", "embeddings"],
      "mock_response": "Deterministic grounded response for testing."
    }
  },
  "default_provider": "mock"
}
```

---

## 3. Environment Variable Injection
To prevent credential leaks:
- API keys are **never stored** in `providers.json`.
- The `api_key_env` property points to an environment variable name (e.g. `GEMINI_API_KEY`, `OPENAI_API_KEY`).
- At runtime, `ProviderRegistry` resolves the key from `os.environ`.
- If credentials are absent, the provider falls back safely or delegates to `mock`.

---

## 4. Supported Provider Profiles

| Provider Profile | Target Runtime | Base URL | Auth Mechanism | Primary Use Case |
|---|---|---|---|---|
| `gemini` | Google DeepMind Gemini 3.8 Flash | `https://generativelanguage.googleapis.com` | `GEMINI_API_KEY` | Production Reasoning & Deep-Path |
| `ollama` | Local Ollama Daemon | `http://localhost:11434` | None / Local | Offline Development & Local Inference |
| `vllm` | High-throughput local vLLM | `http://localhost:8000/v1` | `VLLM_API_KEY` (optional) | High-concurrency Production Serving |
| `lm_studio` | LM Studio Local Server | `http://localhost:1234/v1` | None / Local | Local interactive debugging |
| `openai_compatible` | Any standard OpenAI endpoint | Custom `base_url` | `OPENAI_API_KEY` | Third-party proxy or enterprise gateway |
| `mock` | In-memory Deterministic Mock | N/A | None | Automated unit & regression test suite |

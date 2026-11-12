"""
LiteLLM Provider Adapter for HALO RAG Studio.

Provides unified inference across Gemini, Ollama, vLLM, and OpenAI-compatible gateways.
Falls back safely to deterministic mock inference in offline test environments.
"""

import time
from typing import Optional
from src.providers.provider_registry import ProviderRegistry, ResolvedProvider
from src.providers.schemas import ModelGenerationRequest, ModelGenerationResponse


class LiteLLMAdapter:
    """
    Adapter interfacing LiteLLM completions with HALO RAG Studio.
    """

    def __init__(self, registry: Optional[ProviderRegistry] = None):
        self.registry = registry or ProviderRegistry()

    def generate(self, req: ModelGenerationRequest) -> ModelGenerationResponse:
        start_time = time.time()
        resolved: ResolvedProvider = self.registry.get_provider(req.provider_override)
        cfg = resolved.config

        # 1. Deterministic Mock Provider Handling (Offline Testing)
        if cfg.provider_type == "mock" or not resolved.is_authenticated:
            elapsed = (time.time() - start_time) * 1000.0
            mock_text = cfg.mock_response or f"[MOCK:{cfg.model}] Generated response for prompt: {req.prompt[:60]}..."
            return ModelGenerationResponse(
                text=mock_text,
                provider_name=resolved.name,
                model_name=cfg.model,
                latency_ms=elapsed,
                usage={"prompt_tokens": len(req.prompt.split()), "completion_tokens": len(mock_text.split())}
            )

        # 2. Real LiteLLM API Invocation
        try:
            import litellm  # type: ignore
            litellm.suppress_debug_info = True
            litellm.set_verbose = False

            messages = []
            if req.system_instruction:
                messages.append({"role": "system", "content": req.system_instruction})
            messages.append({"role": "user", "content": req.prompt})

            kwargs = {
                "model": cfg.model,
                "messages": messages,
                "temperature": req.temperature,
                "max_tokens": req.max_tokens,
                "timeout": cfg.timeout_seconds,
            }

            if cfg.base_url:
                kwargs["api_base"] = cfg.base_url
            if resolved.api_key:
                kwargs["api_key"] = resolved.api_key

            response = litellm.completion(**kwargs)
            elapsed = (time.time() - start_time) * 1000.0

            text_output = response.choices[0].message.content or ""
            usage_dict = {
                "prompt_tokens": getattr(response.usage, "prompt_tokens", 0),
                "completion_tokens": getattr(response.usage, "completion_tokens", 0),
            }

            return ModelGenerationResponse(
                text=text_output,
                provider_name=resolved.name,
                model_name=cfg.model,
                latency_ms=elapsed,
                usage=usage_dict
            )
        except Exception as e:
            elapsed = (time.time() - start_time) * 1000.0
            # Return safe fallback with error description
            return ModelGenerationResponse(
                text=f"[PROVIDER_FALLBACK] Request failed: {type(e).__name__}: {str(e)}",
                provider_name=resolved.name,
                model_name=cfg.model,
                latency_ms=elapsed,
                usage={}
            )

"""Unit tests for LiteLLM Provider Registry and adapter configuration."""

import os
import pytest
from src.providers.provider_registry import ProviderRegistry
from src.providers.litellm_provider import LiteLLMAdapter
from src.providers.schemas import ModelGenerationRequest


def test_provider_registry_loading():
    registry = ProviderRegistry("providers.json")
    providers = registry.list_providers()
    assert "gemini" in providers
    assert "ollama" in providers
    assert "vllm" in providers
    assert "mock" in providers
    assert registry.registry.default_provider == "mock"


def test_deterministic_mock_provider_generation():
    registry = ProviderRegistry("providers.json")
    adapter = LiteLLMAdapter(registry)

    req = ModelGenerationRequest(
        prompt="Test prompt for system verification",
        provider_override="mock",
        temperature=0.0
    )
    resp = adapter.generate(req)
    assert resp.provider_name == "mock"
    assert "Deterministic grounded response" in resp.text
    assert resp.latency_ms >= 0.0


def test_environment_variable_resolution(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-secret-key-12345")
    registry = ProviderRegistry("providers.json")
    resolved = registry.get_provider("openai_compatible")
    assert resolved.is_authenticated is True
    assert resolved.api_key == "test-secret-key-12345"

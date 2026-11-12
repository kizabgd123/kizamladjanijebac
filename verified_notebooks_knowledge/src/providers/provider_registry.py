"""
Provider Registry Manager for HALO RAG Studio.

Loads providers.json, validates schemas, and securely resolves API keys from os.environ.
"""

from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Optional
from src.providers.schemas import ProviderConfig, ProviderRegistryConfig


class ProviderRegistry:
    """
    Manages provider configuration profiles and environment variable credential injection.
    """

    def __init__(self, config_path: str = "providers.json"):
        self.config_path = config_path
        self.registry: ProviderRegistryConfig = self._load_config()

    def _load_config(self) -> ProviderRegistryConfig:
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Provider registry configuration file not found: {self.config_path}")

        with open(self.config_path, "r", encoding="utf-8") as f:
            raw = json.load(f)

        return ProviderRegistryConfig(**raw)

    def get_provider(self, name: Optional[str] = None) -> ResolvedProvider:
        target_name = name or self.registry.default_provider
        if target_name not in self.registry.providers:
            raise KeyError(f"Provider '{target_name}' not configured in {self.config_path}")

        cfg = self.registry.providers[target_name]
        api_key: Optional[str] = None
        if cfg.api_key_env:
            api_key = os.environ.get(cfg.api_key_env)

        return ResolvedProvider(name=target_name, config=cfg, api_key=api_key)

    def list_providers(self) -> List[str]:
        return list(self.registry.providers.keys())


class ResolvedProvider:
    def __init__(self, name: str, config: ProviderConfig, api_key: Optional[str]):
        self.name = name
        self.config = config
        self.api_key = api_key

    @property
    def is_authenticated(self) -> bool:
        if self.config.provider_type == "mock":
            return True
        if self.config.provider_type == "ollama":
            return True
        return bool(self.api_key)


Tuple_Resolved = ResolvedProvider

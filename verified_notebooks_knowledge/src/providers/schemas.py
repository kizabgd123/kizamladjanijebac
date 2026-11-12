"""Pydantic schemas for Provider Registry and Model Requests."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ProviderConfig(BaseModel):
    provider_type: str = Field(..., description="Provider backend type, e.g. google_genai, openai_compatible, ollama, mock")
    model: str = Field(..., description="Model identifier")
    base_url: Optional[str] = Field(None, description="Base API endpoint URL if applicable")
    api_key_env: Optional[str] = Field(None, description="Environment variable name holding API key")
    timeout_seconds: int = Field(30, description="Request timeout in seconds")
    max_retries: int = Field(2, description="Maximum retry count on transient network errors")
    capabilities: List[str] = Field(default_factory=list, description="Supported capabilities")
    mock_response: Optional[str] = Field(None, description="Static response if mock provider")


class ProviderRegistryConfig(BaseModel):
    providers: Dict[str, ProviderConfig]
    default_provider: str = Field("mock", description="Default provider profile name")


class ModelGenerationRequest(BaseModel):
    prompt: str
    system_instruction: Optional[str] = None
    temperature: float = 0.2
    max_tokens: int = 1024
    provider_override: Optional[str] = None


class ModelGenerationResponse(BaseModel):
    text: str
    provider_name: str
    model_name: str
    latency_ms: float
    usage: Dict[str, int] = Field(default_factory=dict)

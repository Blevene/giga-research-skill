"""Configuration loaded from environment variables and .env file."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Resolve the skill root directory (two levels up from this file: src/giga_research/config.py -> project root)
_SKILL_ROOT = Path(__file__).resolve().parent.parent.parent


class Config(BaseModel):
    """Application configuration with secrets hidden from repr."""

    claude_api_key: str | None = Field(default=None, repr=False)
    openai_api_key: str | None = Field(default=None, repr=False)
    gemini_api_key: str | None = Field(default=None, repr=False)

    request_timeout: int = 900
    max_retries: int = 3
    citation_validation_depth: int = Field(default=0, ge=0, le=3)
    output_dir: Path = Path("research-output")

    @property
    def available_providers(self) -> list[str]:
        """Return list of providers with configured API keys."""
        providers: list[str] = []
        if self.claude_api_key:
            providers.append("claude")
        if self.openai_api_key:
            providers.append("openai")
        if self.gemini_api_key:
            providers.append("gemini")
        return providers

    @classmethod
    def from_env(cls, env_file: Path | None = None) -> Config:
        """Load configuration from .env file (in skill root) then environment variables.

        The .env file at the skill root is loaded first, but existing environment
        variables take precedence (override=False by default in dotenv).
        """
        dotenv_path = env_file or _SKILL_ROOT / ".env"
        load_dotenv(dotenv_path)
        return cls(
            claude_api_key=os.environ.get("ANTHROPIC_API_KEY"),
            openai_api_key=os.environ.get("OPENAI_API_KEY"),
            gemini_api_key=os.environ.get("GEMINI_API_KEY"),
        )

"""Shared test fixtures for giga_research."""

from __future__ import annotations

import pytest

from giga_research.config import Config


@pytest.fixture
def config_no_keys() -> Config:
    """Config with no API keys set."""
    return Config()


@pytest.fixture
def config_all_keys() -> Config:
    """Config with all API keys set."""
    return Config(
        claude_api_key="test-claude-key",
        openai_api_key="test-openai-key",
        gemini_api_key="test-gemini-key",
    )

"""Tests for Config loading and validation."""

from __future__ import annotations

import os
from unittest.mock import patch

from giga_research.config import Config


def test_config_defaults():
    c = Config()
    assert c.claude_api_key is None
    assert c.openai_api_key is None
    assert c.gemini_api_key is None
    assert c.request_timeout == 300
    assert c.max_retries == 3
    assert c.citation_validation_depth == 0


def test_config_available_providers_none():
    c = Config()
    assert c.available_providers == []


def test_config_available_providers_some():
    c = Config(claude_api_key="key1", gemini_api_key="key2")
    providers = c.available_providers
    assert "claude" in providers
    assert "gemini" in providers
    assert "openai" not in providers


def test_config_available_providers_all():
    c = Config(
        claude_api_key="k1",
        openai_api_key="k2",
        gemini_api_key="k3",
    )
    assert len(c.available_providers) == 3


def test_config_from_env():
    env = {
        "ANTHROPIC_API_KEY": "claude-secret",
        "OPENAI_API_KEY": "openai-secret",
        "GEMINI_API_KEY": "gemini-secret",
    }
    with patch.dict(os.environ, env, clear=False):
        c = Config.from_env()
    assert c.claude_api_key == "claude-secret"
    assert c.openai_api_key == "openai-secret"
    assert c.gemini_api_key == "gemini-secret"


def test_config_from_env_partial():
    env = {"OPENAI_API_KEY": "only-openai"}
    with patch.dict(os.environ, env, clear=False):
        cleaned = {k: v for k, v in os.environ.items()}
        cleaned.pop("ANTHROPIC_API_KEY", None)
        cleaned.pop("GEMINI_API_KEY", None)
        with patch.dict(os.environ, cleaned, clear=True):
            c = Config.from_env()
    assert c.openai_api_key == "only-openai"
    assert c.claude_api_key is None
    assert c.gemini_api_key is None


def test_config_secrets_not_in_repr():
    c = Config(claude_api_key="super-secret")
    r = repr(c)
    assert "super-secret" not in r


def test_config_validation_depth_range():
    c = Config(citation_validation_depth=3)
    assert c.citation_validation_depth == 3

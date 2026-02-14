"""Tests for OpenAI research client."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from giga_research.clients.openai_client import OpenAIClient
from giga_research.config import Config


@pytest.fixture
def config_with_openai() -> Config:
    return Config(openai_api_key="test-key", request_timeout=10, max_retries=0)


def test_is_available_true(config_with_openai: Config):
    client = OpenAIClient(config_with_openai)
    assert client.is_available() is True


def test_is_available_false():
    client = OpenAIClient(Config())
    assert client.is_available() is False


async def test_do_research_returns_result(config_with_openai: Config):
    mock_choice = MagicMock()
    mock_choice.message.content = "# OpenAI Research\n\nFindings."

    mock_response = MagicMock()
    mock_response.choices = [mock_choice]
    mock_response.usage.prompt_tokens = 200
    mock_response.usage.completion_tokens = 800
    mock_response.model = "gpt-4o"

    mock_client = MagicMock()
    mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

    with patch("giga_research.clients.openai_client.AsyncOpenAI", return_value=mock_client):
        client = OpenAIClient(config_with_openai)
        result = await client.research("test prompt")

    assert result.provider == "openai"
    assert "OpenAI Research" in result.content
    assert result.metadata.tokens_used == 1000

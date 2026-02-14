"""Tests for Claude research client."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from giga_research.clients.claude import ClaudeClient
from giga_research.config import Config


@pytest.fixture
def config_with_claude() -> Config:
    return Config(claude_api_key="test-key", request_timeout=10, max_retries=0)


@pytest.fixture
def config_no_claude() -> Config:
    return Config()


def test_is_available_true(config_with_claude: Config):
    client = ClaudeClient(config_with_claude)
    assert client.is_available() is True


def test_is_available_false(config_no_claude: Config):
    client = ClaudeClient(config_no_claude)
    assert client.is_available() is False


async def test_do_research_returns_result(config_with_claude: Config):
    mock_message = MagicMock()
    mock_message.content = [MagicMock(text="# Research Report\n\nFindings here.")]
    mock_message.usage.input_tokens = 100
    mock_message.usage.output_tokens = 500
    mock_message.model = "claude-sonnet-4-5-20250929"

    mock_client = MagicMock()
    mock_client.messages.create = AsyncMock(return_value=mock_message)

    with patch("giga_research.clients.claude.AsyncAnthropic", return_value=mock_client):
        client = ClaudeClient(config_with_claude)
        result = await client.research("test prompt")

    assert result.provider == "claude"
    assert "Research Report" in result.content
    assert result.metadata.model == "claude-sonnet-4-5-20250929"
    assert result.metadata.tokens_used == 600

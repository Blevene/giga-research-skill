"""Tests for OpenAI deep research client using Responses API."""

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
    # Mock the initial response from responses.create (background=True)
    mock_initial = MagicMock()
    mock_initial.id = "resp-123"
    mock_initial.status = "in_progress"

    # Mock the completed response from responses.retrieve
    mock_completed = MagicMock()
    mock_completed.id = "resp-123"
    mock_completed.status = "completed"
    mock_completed.output_text = "# OpenAI Deep Research\n\nFindings here."
    mock_completed.usage.input_tokens = 200
    mock_completed.usage.output_tokens = 800
    mock_completed.model = "o3-deep-research"

    mock_client = MagicMock()
    mock_client.responses.create = AsyncMock(return_value=mock_initial)
    mock_client.responses.retrieve = AsyncMock(return_value=mock_completed)

    with (
        patch("giga_research.clients.openai_client.AsyncOpenAI", return_value=mock_client),
        patch("giga_research.clients.openai_client.asyncio.sleep"),
    ):
        client = OpenAIClient(config_with_openai)
        result = await client.research("test prompt")

    assert result.provider == "openai"
    assert "OpenAI Deep Research" in result.content
    assert result.metadata.model == "o3-deep-research"
    assert result.metadata.tokens_used == 1000

    # Verify Responses API was called with correct params
    mock_client.responses.create.assert_awaited_once()
    call_kwargs = mock_client.responses.create.call_args.kwargs
    assert call_kwargs["model"] == "o3-deep-research"
    assert call_kwargs["background"] is True


async def test_do_research_handles_failure(config_with_openai: Config):
    mock_initial = MagicMock()
    mock_initial.id = "resp-456"
    mock_initial.status = "in_progress"

    mock_failed = MagicMock()
    mock_failed.id = "resp-456"
    mock_failed.status = "failed"
    mock_failed.error = MagicMock(message="Rate limit exceeded")

    mock_client = MagicMock()
    mock_client.responses.create = AsyncMock(return_value=mock_initial)
    mock_client.responses.retrieve = AsyncMock(return_value=mock_failed)

    with (
        patch("giga_research.clients.openai_client.AsyncOpenAI", return_value=mock_client),
        patch("giga_research.clients.openai_client.asyncio.sleep"),
    ):
        client = OpenAIClient(config_with_openai)
        from giga_research.errors import ProviderError

        with pytest.raises(ProviderError, match="failed"):
            await client.research("test prompt")

"""Tests for OpenAI deep research client using Responses API."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from giga_research.clients.openai_client import _MODEL, OpenAIClient
from giga_research.config import Config


@pytest.fixture
def config_with_openai() -> Config:
    return Config(openai_api_key="test-key", request_timeout=10, max_retries=0)


def _url_annotation(url: str, title: str) -> MagicMock:
    ann = MagicMock(spec=["type", "url", "title", "start_index", "end_index"])
    ann.type = "url_citation"
    ann.url = url
    ann.title = title
    return ann


def _output_message(text: str, annotations: list[MagicMock]) -> MagicMock:
    block = MagicMock(spec=["type", "text", "annotations"])
    block.type = "output_text"
    block.text = text
    block.annotations = annotations
    item = MagicMock(spec=["type", "content"])
    item.type = "message"
    item.content = [block]
    return item


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
    mock_completed.output = [
        _output_message(
            "Findings here.",
            [_url_annotation("https://example.com/source", "A Source")],
        )
    ]
    mock_completed.usage.input_tokens = 200
    mock_completed.usage.output_tokens = 800
    mock_completed.model = _MODEL

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
    assert result.metadata.model == _MODEL
    assert result.metadata.tokens_used == 1000

    # Citations extracted from output-text annotations
    assert len(result.citations) == 1
    assert result.citations[0].url == "https://example.com/source"
    assert result.citations[0].title == "A Source"

    # Verify Responses API was called with current model + web_search tool
    mock_client.responses.create.assert_awaited_once()
    call_kwargs = mock_client.responses.create.call_args.kwargs
    assert call_kwargs["model"] == _MODEL
    assert call_kwargs["background"] is True
    assert any(t.get("type") == "web_search" for t in call_kwargs["tools"])


async def test_do_research_handles_failure(config_with_openai: Config):
    mock_initial = MagicMock()
    mock_initial.id = "resp-456"
    mock_initial.status = "in_progress"

    mock_failed = MagicMock()
    mock_failed.id = "resp-456"
    mock_failed.status = "failed"
    mock_failed.error = MagicMock(message="Internal server error")

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


async def test_rate_limit_failure_raises_rate_limit_error(config_with_openai: Config):
    from giga_research.errors import ProviderRateLimitError

    mock_initial = MagicMock()
    mock_initial.id = "resp-789"
    mock_initial.status = "in_progress"

    mock_failed = MagicMock()
    mock_failed.id = "resp-789"
    mock_failed.status = "failed"
    mock_failed.error = MagicMock(
        message="Rate limit reached for gpt-5.5-pro on tokens per min (TPM): Limit 1000000. try again in 12s"
    )

    mock_client = MagicMock()
    mock_client.responses.create = AsyncMock(return_value=mock_initial)
    mock_client.responses.retrieve = AsyncMock(return_value=mock_failed)

    with (
        patch("giga_research.clients.openai_client.AsyncOpenAI", return_value=mock_client),
        patch("giga_research.clients.openai_client.asyncio.sleep"),
    ):
        client = OpenAIClient(config_with_openai)
        with pytest.raises(ProviderRateLimitError) as exc_info:
            await client.research("test prompt")
    assert exc_info.value.retry_after_s == 12.0

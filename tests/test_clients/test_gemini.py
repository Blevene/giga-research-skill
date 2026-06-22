"""Tests for Gemini deep research client using Interactions API."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from giga_research.clients.gemini import _AGENT, GeminiClient
from giga_research.config import Config
from giga_research.errors import ProviderError


@pytest.fixture
def config_with_gemini() -> Config:
    return Config(gemini_api_key="test-key", request_timeout=10, max_retries=0)


def _annotation(url: str, title: str) -> MagicMock:
    """A url-citation annotation (newer schema: url/title directly on the annotation)."""
    ann = MagicMock(spec=["url", "title", "cited_text", "source"])
    ann.url = url
    ann.title = title
    ann.cited_text = ""
    ann.source = None
    return ann


def _text_block(text: str, annotations: list[MagicMock]) -> MagicMock:
    block = MagicMock(spec=["text", "annotations"])
    block.text = text
    block.annotations = annotations
    return block


def _step(blocks: list[MagicMock]) -> MagicMock:
    step = MagicMock(spec=["content"])
    step.content = blocks
    return step


def test_is_available_true(config_with_gemini: Config):
    client = GeminiClient(config_with_gemini)
    assert client.is_available() is True


def test_is_available_false():
    client = GeminiClient(Config())
    assert client.is_available() is False


async def test_do_research_returns_result(config_with_gemini: Config):
    # Newer (2.x) schema: output_text + steps + usage.total_tokens
    mock_initial = MagicMock(spec=["id", "status"])
    mock_initial.id = "interaction-123"
    mock_initial.status = "in_progress"

    block = _text_block("Findings.", [_annotation("https://example.com/a", "Source A")])
    mock_done = MagicMock(spec=["id", "status", "output_text", "steps", "outputs", "usage", "model", "error"])
    mock_done.id = "interaction-123"
    mock_done.status = "completed"
    mock_done.output_text = "# Gemini Deep Research\n\nFindings."
    mock_done.steps = [_step([block])]
    mock_done.outputs = []
    mock_done.model = _AGENT
    mock_done.usage = MagicMock(spec=["total_tokens"])
    mock_done.usage.total_tokens = 4242

    mock_client_instance = MagicMock()
    mock_client_instance.interactions.create.return_value = mock_initial
    mock_client_instance.interactions.get.return_value = mock_done

    with patch("giga_research.clients.gemini.genai") as mock_genai:
        mock_genai.Client.return_value = mock_client_instance
        with patch("giga_research.clients.gemini.asyncio.sleep"):
            client = GeminiClient(config_with_gemini)
            result = await client.research("test prompt")

    assert result.provider == "gemini"
    assert "Gemini Deep Research" in result.content
    assert result.metadata.model == _AGENT
    assert result.metadata.tokens_used == 4242

    # Citations extracted from annotations
    assert len(result.citations) == 1
    assert result.citations[0].url == "https://example.com/a"
    assert result.citations[0].title == "Source A"

    # Interactions API called with the current agent ID
    mock_client_instance.interactions.create.assert_called_once()
    call_kwargs = mock_client_instance.interactions.create.call_args.kwargs
    assert call_kwargs.get("agent") == _AGENT
    assert call_kwargs.get("background") is True


async def test_do_research_reads_legacy_outputs(config_with_gemini: Config):
    """Falls back to the 1.x `outputs[].text` shape when output_text/steps are absent."""
    mock_initial = MagicMock(spec=["id", "status"])
    mock_initial.id = "interaction-legacy"
    mock_initial.status = "in_progress"

    out_item = MagicMock(spec=["text"])
    out_item.text = "Legacy report text."

    mock_done = MagicMock(spec=["id", "status", "outputs", "usage", "model", "error"])
    mock_done.id = "interaction-legacy"
    mock_done.status = "completed"
    mock_done.outputs = [out_item]
    mock_done.model = _AGENT
    mock_done.usage = MagicMock(spec=["total_tokens"])
    mock_done.usage.total_tokens = 100

    mock_client_instance = MagicMock()
    mock_client_instance.interactions.create.return_value = mock_initial
    mock_client_instance.interactions.get.return_value = mock_done

    with patch("giga_research.clients.gemini.genai") as mock_genai:
        mock_genai.Client.return_value = mock_client_instance
        with patch("giga_research.clients.gemini.asyncio.sleep"):
            client = GeminiClient(config_with_gemini)
            result = await client.research("test prompt")

    assert "Legacy report text." in result.content
    assert result.citations == []


async def test_do_research_handles_budget_exceeded(config_with_gemini: Config):
    """Terminal statuses beyond `failed` (e.g. budget_exceeded) raise ProviderError."""
    mock_initial = MagicMock(spec=["id", "status"])
    mock_initial.id = "interaction-456"
    mock_initial.status = "in_progress"

    mock_terminal = MagicMock(spec=["id", "status", "error"])
    mock_terminal.id = "interaction-456"
    mock_terminal.status = "budget_exceeded"
    mock_terminal.error = "ran out of budget"

    mock_client_instance = MagicMock()
    mock_client_instance.interactions.create.return_value = mock_initial
    mock_client_instance.interactions.get.return_value = mock_terminal

    with patch("giga_research.clients.gemini.genai") as mock_genai:
        mock_genai.Client.return_value = mock_client_instance
        with patch("giga_research.clients.gemini.asyncio.sleep"):
            client = GeminiClient(config_with_gemini)
            with pytest.raises(ProviderError, match="budget_exceeded"):
                await client.research("test prompt")

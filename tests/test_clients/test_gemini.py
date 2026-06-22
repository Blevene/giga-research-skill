"""Tests for Gemini deep research client using Interactions API."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from giga_research.clients.gemini import _AGENT, GeminiClient
from giga_research.config import Config
from giga_research.errors import ProviderError, ProviderRateLimitError


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


def _step(blocks: list[MagicMock], step_type: str = "model_output") -> MagicMock:
    step = MagicMock(spec=["content", "type"])
    step.type = step_type
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

    block = _text_block("# Gemini Deep Research\n\nFindings.", [_annotation("https://example.com/a", "Source A")])
    mock_done = MagicMock(spec=["id", "status", "output_text", "steps", "outputs", "usage", "model", "error"])
    mock_done.id = "interaction-123"
    mock_done.status = "completed"
    # output_text is only the final segment — code must use steps, not this.
    mock_done.output_text = "PARTIAL_ONLY"
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
    assert "PARTIAL_ONLY" not in result.content  # output_text must NOT be used as the body
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


async def test_skips_user_input_and_concatenates_model_output_steps(config_with_gemini: Config):
    """user_input steps are skipped; multiple model_output steps are joined in order."""
    mock_initial = MagicMock(spec=["id", "status"])
    mock_initial.id = "interaction-multi"
    mock_initial.status = "in_progress"

    user_step = _step([_text_block("the original prompt echo", [])], step_type="user_input")
    out1 = _step([_text_block("# Title and intro.\n\n", [])])
    out2 = _step([_text_block("## Body section with detail.", [])])

    mock_done = MagicMock(spec=["id", "status", "output_text", "steps", "usage", "model", "error"])
    mock_done.id = "interaction-multi"
    mock_done.status = "completed"
    mock_done.output_text = "## Body section with detail."  # only the last segment
    mock_done.steps = [user_step, out1, out2]
    mock_done.model = _AGENT
    mock_done.usage = MagicMock(spec=["total_tokens"])
    mock_done.usage.total_tokens = 10

    mock_client_instance = MagicMock()
    mock_client_instance.interactions.create.return_value = mock_initial
    mock_client_instance.interactions.get.return_value = mock_done

    with patch("giga_research.clients.gemini.genai") as mock_genai:
        mock_genai.Client.return_value = mock_client_instance
        with patch("giga_research.clients.gemini.asyncio.sleep"):
            result = await GeminiClient(config_with_gemini).research("test prompt")

    assert "Title and intro" in result.content  # earlier section preserved
    assert "Body section with detail" in result.content
    assert "the original prompt echo" not in result.content  # user_input skipped


async def test_rate_limit_failure_raises_rate_limit_error(config_with_gemini: Config):
    mock_initial = MagicMock(spec=["id", "status"])
    mock_initial.id = "interaction-rl"
    mock_initial.status = "in_progress"

    mock_failed = MagicMock(spec=["id", "status", "error"])
    mock_failed.id = "interaction-rl"
    mock_failed.status = "failed"
    mock_failed.error = "Error code: 429 - rate limit exceeded, try again in 30 seconds"

    mock_client_instance = MagicMock()
    mock_client_instance.interactions.create.return_value = mock_initial
    mock_client_instance.interactions.get.return_value = mock_failed

    with patch("giga_research.clients.gemini.genai") as mock_genai:
        mock_genai.Client.return_value = mock_client_instance
        with (
            patch("giga_research.clients.gemini.asyncio.sleep"),
            pytest.raises(ProviderRateLimitError) as exc_info,
        ):
            await GeminiClient(config_with_gemini).research("test prompt")
    assert exc_info.value.retry_after_s == 30.0

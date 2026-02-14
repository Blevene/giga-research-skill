"""Tests for Gemini deep research client using Interactions API."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from giga_research.clients.gemini import GeminiClient
from giga_research.config import Config


@pytest.fixture
def config_with_gemini() -> Config:
    return Config(gemini_api_key="test-key", request_timeout=10, max_retries=0)


def test_is_available_true(config_with_gemini: Config):
    client = GeminiClient(config_with_gemini)
    assert client.is_available() is True


def test_is_available_false():
    client = GeminiClient(Config())
    assert client.is_available() is False


async def test_do_research_returns_result(config_with_gemini: Config):
    # Mock the interaction object returned by create
    mock_interaction_initial = MagicMock()
    mock_interaction_initial.id = "interaction-123"
    mock_interaction_initial.status = "in_progress"

    # Mock the completed interaction returned by get
    mock_output = MagicMock()
    mock_output.text = "# Gemini Deep Research\n\nFindings."

    mock_interaction_done = MagicMock()
    mock_interaction_done.id = "interaction-123"
    mock_interaction_done.status = "completed"
    mock_interaction_done.outputs = [mock_output]

    mock_client_instance = MagicMock()
    mock_client_instance.interactions.create.return_value = mock_interaction_initial
    mock_client_instance.interactions.get.return_value = mock_interaction_done

    with patch("giga_research.clients.gemini.genai") as mock_genai:
        mock_genai.Client.return_value = mock_client_instance
        # Patch asyncio.sleep to not actually wait
        with patch("giga_research.clients.gemini.asyncio.sleep"):
            client = GeminiClient(config_with_gemini)
            result = await client.research("test prompt")

    assert result.provider == "gemini"
    assert "Gemini Deep Research" in result.content
    assert result.metadata.model == "deep-research-pro-preview-12-2025"

    # Verify interactions API was called correctly
    mock_client_instance.interactions.create.assert_called_once()
    call_kwargs = mock_client_instance.interactions.create.call_args
    assert call_kwargs.kwargs.get("agent") == "deep-research-pro-preview-12-2025"
    assert call_kwargs.kwargs.get("background") is True


async def test_do_research_handles_failure(config_with_gemini: Config):
    mock_interaction_initial = MagicMock()
    mock_interaction_initial.id = "interaction-456"
    mock_interaction_initial.status = "in_progress"

    mock_interaction_failed = MagicMock()
    mock_interaction_failed.id = "interaction-456"
    mock_interaction_failed.status = "failed"
    mock_interaction_failed.error = "Research failed due to quota"

    mock_client_instance = MagicMock()
    mock_client_instance.interactions.create.return_value = mock_interaction_initial
    mock_client_instance.interactions.get.return_value = mock_interaction_failed

    with patch("giga_research.clients.gemini.genai") as mock_genai:
        mock_genai.Client.return_value = mock_client_instance
        with patch("giga_research.clients.gemini.asyncio.sleep"):
            client = GeminiClient(config_with_gemini)
            from giga_research.errors import ProviderError

            with pytest.raises(ProviderError, match="failed"):
                await client.research("test prompt")

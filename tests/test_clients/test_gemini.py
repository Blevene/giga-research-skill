"""Tests for Gemini research client."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

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
    mock_response = MagicMock()
    mock_response.text = "# Gemini Research\n\nFindings."
    mock_response.usage_metadata.prompt_token_count = 150
    mock_response.usage_metadata.candidates_token_count = 700

    mock_generate = AsyncMock(return_value=mock_response)

    mock_client_instance = MagicMock()
    mock_client_instance.aio.models.generate_content = mock_generate

    with patch("giga_research.clients.gemini.genai") as mock_genai:
        mock_genai.Client.return_value = mock_client_instance
        mock_genai.types.GenerateContentConfig = MagicMock()
        client = GeminiClient(config_with_gemini)
        result = await client.research("test prompt")

    assert result.provider == "gemini"
    assert "Gemini Research" in result.content
    assert result.metadata.tokens_used == 850

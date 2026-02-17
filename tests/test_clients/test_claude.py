"""Tests for Claude research client."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from giga_research.clients.claude import ClaudeClient, _BETA
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


def _make_citation(cited_text: str, url: str, title: str) -> MagicMock:
    """Create a mock CitationsWebSearchResultLocation."""
    cite = MagicMock()
    cite.type = "web_search_result_location"
    cite.cited_text = cited_text
    cite.url = url
    cite.title = title
    return cite


def _make_search_result(url: str, title: str) -> MagicMock:
    """Create a mock WebSearchResultBlock."""
    result = MagicMock()
    result.type = "web_search_result"
    result.url = url
    result.title = title
    result.encrypted_content = "enc"
    return result


async def test_do_research_returns_result(config_with_claude: Config):
    # Simulate mixed content blocks (text + web search results)
    text_block = MagicMock(text="# Research Report\n\nFindings here.")
    text_block.type = "text"
    text_block.citations = None

    search_block = MagicMock(spec=[])  # No .text attribute — simulates a server_tool_use block

    text_block2 = MagicMock(text="More findings with citations.")
    text_block2.type = "text"
    text_block2.citations = None

    mock_message = MagicMock()
    mock_message.content = [text_block, search_block, text_block2]
    mock_message.usage.input_tokens = 100
    mock_message.usage.output_tokens = 500
    mock_message.model = "claude-sonnet-4-6"

    mock_client = MagicMock()
    mock_client.beta.messages.create = AsyncMock(return_value=mock_message)

    with patch("giga_research.clients.claude.AsyncAnthropic", return_value=mock_client):
        client = ClaudeClient(config_with_claude)
        result = await client.research("test prompt")

    assert result.provider == "claude"
    assert "Research Report" in result.content
    assert "More findings with citations" in result.content
    assert result.metadata.model == "claude-sonnet-4-6"
    assert result.metadata.tokens_used == 600

    # Verify web search tool was included with new 20260209 version
    call_kwargs = mock_client.beta.messages.create.call_args.kwargs
    tools = call_kwargs["tools"]
    assert any(t.get("type") == "web_search_20260209" for t in tools)
    assert _BETA in call_kwargs["betas"]


async def test_extracts_inline_citations_from_text_blocks(config_with_claude: Config):
    """Citations from TextBlock.citations (CitationsWebSearchResultLocation) are extracted."""
    cite1 = _make_citation("Ransomware increased 50%", "https://example.com/report", "Security Report")
    cite2 = _make_citation("LockBit was disrupted", "https://example.com/lockbit", "LockBit Analysis")

    text_block = MagicMock(text="Research with inline citations.")
    text_block.type = "text"
    text_block.citations = [cite1, cite2]

    mock_message = MagicMock()
    mock_message.content = [text_block]
    mock_message.usage.input_tokens = 50
    mock_message.usage.output_tokens = 200
    mock_message.model = "claude-sonnet-4-6"

    mock_client = MagicMock()
    mock_client.beta.messages.create = AsyncMock(return_value=mock_message)

    with patch("giga_research.clients.claude.AsyncAnthropic", return_value=mock_client):
        client = ClaudeClient(config_with_claude)
        result = await client.research("test prompt")

    assert len(result.citations) == 2
    assert result.citations[0].url == "https://example.com/report"
    assert result.citations[0].title == "Security Report"
    assert result.citations[0].text == "Ransomware increased 50%"
    assert result.citations[1].url == "https://example.com/lockbit"


async def test_extracts_citations_from_web_search_result_blocks(config_with_claude: Config):
    """Citations from WebSearchToolResultBlock.content are extracted."""
    search_result1 = _make_search_result("https://example.com/page1", "Page One")
    search_result2 = _make_search_result("https://example.com/page2", "Page Two")

    web_search_block = MagicMock(spec=["type", "content", "tool_use_id"])
    web_search_block.type = "web_search_tool_result"
    web_search_block.content = [search_result1, search_result2]

    text_block = MagicMock(text="Analysis based on search results.")
    text_block.type = "text"
    text_block.citations = None

    mock_message = MagicMock()
    mock_message.content = [web_search_block, text_block]
    mock_message.usage.input_tokens = 50
    mock_message.usage.output_tokens = 200
    mock_message.model = "claude-sonnet-4-6"

    mock_client = MagicMock()
    mock_client.beta.messages.create = AsyncMock(return_value=mock_message)

    with patch("giga_research.clients.claude.AsyncAnthropic", return_value=mock_client):
        client = ClaudeClient(config_with_claude)
        result = await client.research("test prompt")

    assert len(result.citations) == 2
    assert result.citations[0].url == "https://example.com/page1"
    assert result.citations[0].title == "Page One"
    assert result.citations[1].url == "https://example.com/page2"


async def test_deduplicates_citations_across_sources(config_with_claude: Config):
    """Same URL from both inline citation and search result block is not duplicated."""
    shared_url = "https://example.com/shared"

    # Search result block with the URL
    search_result = _make_search_result(shared_url, "Shared Source")
    web_search_block = MagicMock(spec=["type", "content", "tool_use_id"])
    web_search_block.type = "web_search_tool_result"
    web_search_block.content = [search_result]

    # Text block with inline citation referencing the same URL
    cite = _make_citation("Some cited text", shared_url, "Shared Source")
    text_block = MagicMock(text="Analysis text.")
    text_block.type = "text"
    text_block.citations = [cite]

    mock_message = MagicMock()
    mock_message.content = [web_search_block, text_block]
    mock_message.usage.input_tokens = 50
    mock_message.usage.output_tokens = 200
    mock_message.model = "claude-sonnet-4-6"

    mock_client = MagicMock()
    mock_client.beta.messages.create = AsyncMock(return_value=mock_message)

    with patch("giga_research.clients.claude.AsyncAnthropic", return_value=mock_client):
        client = ClaudeClient(config_with_claude)
        result = await client.research("test prompt")

    # Should only have one citation, not two
    assert len(result.citations) == 1
    assert result.citations[0].url == shared_url

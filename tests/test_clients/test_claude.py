"""Tests for Claude research client (bounded single-pass web search)."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from giga_research.clients.claude import _BETA, ClaudeClient
from giga_research.config import Config
from giga_research.errors import ProviderError


@pytest.fixture
def config_with_claude() -> Config:
    return Config(claude_api_key="test-key", request_timeout=10, max_retries=0)


@pytest.fixture
def config_no_claude() -> Config:
    return Config()


def _message(content: list, *, stop_reason: str = "end_turn", in_tok: int = 100, out_tok: int = 500) -> MagicMock:
    msg = MagicMock()
    msg.content = content
    msg.stop_reason = stop_reason
    msg.usage.input_tokens = in_tok
    msg.usage.output_tokens = out_tok
    msg.model = "claude-sonnet-4-6"
    return msg


def _stream_side_effect(*messages: MagicMock) -> list:
    """Build one async-context-manager per stream() call, each yielding a message."""
    cms = []
    for m in messages:
        stream_obj = MagicMock()
        stream_obj.get_final_message = AsyncMock(return_value=m)
        cm = MagicMock()
        cm.__aenter__ = AsyncMock(return_value=stream_obj)
        cm.__aexit__ = AsyncMock(return_value=False)
        cms.append(cm)
    return cms


def _patched_client(*messages: MagicMock) -> MagicMock:
    mock_client = MagicMock()
    mock_client.beta.messages.stream = MagicMock(side_effect=_stream_side_effect(*messages))
    return mock_client


def _text(text: str, citations=None) -> MagicMock:
    b = MagicMock(text=text)
    b.type = "text"
    b.citations = citations
    return b


def _make_citation(cited_text: str, url: str, title: str) -> MagicMock:
    cite = MagicMock()
    cite.type = "web_search_result_location"
    cite.cited_text = cited_text
    cite.url = url
    cite.title = title
    return cite


def _make_search_result(url: str, title: str) -> MagicMock:
    result = MagicMock()
    result.type = "web_search_result"
    result.url = url
    result.title = title
    result.encrypted_content = "enc"
    return result


def _search_block(*results: MagicMock) -> MagicMock:
    block = MagicMock(spec=["type", "content", "tool_use_id"])
    block.type = "web_search_tool_result"
    block.content = list(results)
    return block


def test_is_available_true(config_with_claude: Config):
    assert ClaudeClient(config_with_claude).is_available() is True


def test_is_available_false(config_no_claude: Config):
    assert ClaudeClient(config_no_claude).is_available() is False


async def test_do_research_returns_result(config_with_claude: Config):
    server_use = MagicMock(spec=[])  # server_tool_use-like block, no .text
    mock_client = _patched_client(
        _message([_text("# Research Report\n\nFindings here."), server_use, _text("More findings.")])
    )

    with patch("giga_research.clients.claude.AsyncAnthropic", return_value=mock_client):
        result = await ClaudeClient(config_with_claude).research("test prompt")

    assert result.provider == "claude"
    assert "Research Report" in result.content
    assert "More findings" in result.content
    assert result.metadata.model == "claude-sonnet-4-6"
    assert result.metadata.tokens_used == 600

    # web_search only — web_fetch is deliberately NOT used (it makes Claude unbounded).
    call_kwargs = mock_client.beta.messages.stream.call_args.kwargs
    tools = call_kwargs["tools"]
    assert any(t.get("type") == "web_search_20260209" for t in tools)
    assert not any(t.get("type") == "web_fetch_20260209" for t in tools)
    assert _BETA in call_kwargs["betas"]
    # Clean single-pass run: no forced synthesis follow-up.
    assert mock_client.beta.messages.stream.call_count == 1


async def test_pause_turn_forces_tools_off_synthesis(config_with_claude: Config):
    """If the search pass pauses for more tools, a tools-off synthesis pass is forced."""
    research = _message([_text("Partial findings.")], stop_reason="pause_turn", in_tok=100, out_tok=200)
    synthesis = _message([_text("# Final Report\n\nSynthesis.")], stop_reason="end_turn", in_tok=300, out_tok=400)
    mock_client = _patched_client(research, synthesis)

    with patch("giga_research.clients.claude.AsyncAnthropic", return_value=mock_client):
        result = await ClaudeClient(config_with_claude).research("test prompt")

    assert "Partial findings." in result.content
    assert "Final Report" in result.content
    assert result.metadata.tokens_used == 1000
    assert mock_client.beta.messages.stream.call_count == 2
    final_kwargs = mock_client.beta.messages.stream.call_args_list[-1].kwargs
    assert final_kwargs.get("tool_choice") == {"type": "none"}


async def test_empty_synthesis_raises(config_with_claude: Config):
    """No prose even after the forced synthesis pass -> ProviderError, not empty content."""
    mock_client = _patched_client(_message([MagicMock(spec=[])]), _message([MagicMock(spec=[])]))

    with (
        patch("giga_research.clients.claude.AsyncAnthropic", return_value=mock_client),
        pytest.raises(ProviderError, match="No synthesis"),
    ):
        await ClaudeClient(config_with_claude).research("test prompt")


async def test_extracts_inline_citations_from_text_blocks(config_with_claude: Config):
    cite1 = _make_citation("Ransomware increased 50%", "https://example.com/report", "Security Report")
    cite2 = _make_citation("LockBit was disrupted", "https://example.com/lockbit", "LockBit Analysis")
    mock_client = _patched_client(_message([_text("Research with inline citations.", [cite1, cite2])]))

    with patch("giga_research.clients.claude.AsyncAnthropic", return_value=mock_client):
        result = await ClaudeClient(config_with_claude).research("test prompt")

    assert len(result.citations) == 2
    assert result.citations[0].url == "https://example.com/report"
    assert result.citations[0].title == "Security Report"
    assert result.citations[0].text == "Ransomware increased 50%"
    assert result.citations[1].url == "https://example.com/lockbit"


async def test_extracts_citations_from_web_search_result_blocks(config_with_claude: Config):
    block = _search_block(
        _make_search_result("https://example.com/page1", "Page One"),
        _make_search_result("https://example.com/page2", "Page Two"),
    )
    mock_client = _patched_client(_message([block, _text("Analysis based on search results.")]))

    with patch("giga_research.clients.claude.AsyncAnthropic", return_value=mock_client):
        result = await ClaudeClient(config_with_claude).research("test prompt")

    assert len(result.citations) == 2
    assert result.citations[0].url == "https://example.com/page1"
    assert result.citations[1].url == "https://example.com/page2"


async def test_deduplicates_citations_across_sources(config_with_claude: Config):
    shared_url = "https://example.com/shared"
    block = _search_block(_make_search_result(shared_url, "Shared Source"))
    cite = _make_citation("Some cited text", shared_url, "Shared Source")
    mock_client = _patched_client(_message([block, _text("Analysis text.", [cite])]))

    with patch("giga_research.clients.claude.AsyncAnthropic", return_value=mock_client):
        result = await ClaudeClient(config_with_claude).research("test prompt")

    assert len(result.citations) == 1
    assert result.citations[0].url == shared_url

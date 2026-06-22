"""Tests for unified-report synthesis."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

from giga_research.config import Config
from giga_research.models import Citation, ResearchResult, ResultMetadata
from giga_research.reconciliation.synthesizer import synthesize_report


def _result(provider: str = "gemini", content: str = "Findings about the topic.") -> ResearchResult:
    return ResearchResult(
        provider=provider,
        content=content,
        citations=[],
        metadata=ResultMetadata(model=f"{provider}-model", tokens_used=10, latency_s=1.0),
    )


async def test_returns_none_without_claude_key():
    cfg = Config()  # no claude_api_key
    out = await synthesize_report(cfg, "Topic", {"gemini": _result()}, "matrix", [])
    assert out is None


async def test_returns_none_without_results():
    cfg = Config(claude_api_key="k")
    out = await synthesize_report(cfg, "Topic", {}, "matrix", [])
    assert out is None


async def test_builds_report_from_provider_inputs():
    cfg = Config(claude_api_key="k")
    block = MagicMock()
    block.text = "# Topic — Research Report\n\nUnified synthesis."
    message = MagicMock()
    message.content = [block]
    mock_client = MagicMock()
    mock_client.messages.create = AsyncMock(return_value=message)

    with patch("giga_research.reconciliation.synthesizer.AsyncAnthropic", return_value=mock_client):
        out = await synthesize_report(
            cfg,
            "ATT&CK CTI",
            {"gemini": _result("gemini", "Gemini findings here.")},
            "| provider | topic |\n|---|---|",
            [Citation(text="t", url="https://example.com/a", title="A")],
        )

    assert out is not None
    assert "Research Report" in out
    call = mock_client.messages.create.call_args.kwargs
    assert call["model"] == cfg.claude_model
    user_content = call["messages"][0]["content"]
    # The synthesis prompt carries the provider report + matrix + citations.
    assert "gemini" in user_content
    assert "Gemini findings here." in user_content
    assert "https://example.com/a" in user_content

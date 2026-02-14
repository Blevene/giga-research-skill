"""Tests for the orchestration pipeline."""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest

from giga_research.models import Citation, ResearchResult, ResultMetadata, ValidationStatus
from giga_research.orchestration.pipeline import PipelineResult, run_pipeline


def _make_result(provider: str, content: str, citations: list[Citation] | None = None) -> ResearchResult:
    return ResearchResult(
        provider=provider,
        content=content,
        citations=citations or [],
        metadata=ResultMetadata(model=f"{provider}-model", tokens_used=100, latency_s=1.0),
    )


class FakeClient:
    """Fake client that returns a predetermined result."""

    def __init__(self, provider_name: str, content: str, citations: list[Citation] | None = None):
        self.provider_name = provider_name
        self._result = _make_result(provider_name, content, citations)

    def is_available(self) -> bool:
        return True

    async def research(self, prompt: str) -> ResearchResult:
        return self._result


class FailingClient:
    """Fake client that raises on research."""

    def __init__(self, provider_name: str, error_msg: str = "API error"):
        self.provider_name = provider_name
        self._error_msg = error_msg

    def is_available(self) -> bool:
        return True

    async def research(self, prompt: str) -> ResearchResult:
        raise RuntimeError(self._error_msg)


@pytest.mark.asyncio
async def test_successful_three_provider_run(session_dir, config_no_keys):
    """All three providers succeed."""
    clients = [
        FakeClient("claude", "## Introduction\nClaude findings.\n## Methods\nClaude methods."),
        FakeClient("openai", "## Introduction\nOpenAI findings.\n## Analysis\nOpenAI analysis."),
        FakeClient("gemini", "## Introduction\nGemini findings.\n## Methods\nGemini methods."),
    ]

    result = await run_pipeline(session_dir, depth=0, config=config_no_keys, clients=clients)

    assert set(result.providers_used) == {"claude", "openai", "gemini"}
    assert result.providers_failed == {}
    assert "Introduction" in result.topics_identified
    assert (session_dir / "comparison-matrix.md").exists()
    assert (session_dir / "validation-log.md").exists()
    assert (session_dir / "meta.json").exists()
    assert (session_dir / "raw" / "claude.md").exists()
    assert (session_dir / "raw" / "openai.md").exists()
    assert (session_dir / "raw" / "gemini.md").exists()


@pytest.mark.asyncio
async def test_partial_failure(session_dir, config_no_keys):
    """One provider fails, two succeed."""
    clients = [
        FakeClient("claude", "## Topic A\nClaude on A."),
        FailingClient("openai", "timeout"),
        FakeClient("gemini", "## Topic A\nGemini on A."),
    ]

    result = await run_pipeline(session_dir, depth=0, config=config_no_keys, clients=clients)

    assert set(result.providers_used) == {"claude", "gemini"}
    assert "openai" in result.providers_failed
    assert "timeout" in result.providers_failed["openai"]
    assert (session_dir / "raw" / "claude.md").exists()
    assert not (session_dir / "raw" / "openai.md").exists()


@pytest.mark.asyncio
async def test_all_providers_fail(session_dir, config_no_keys):
    """All providers fail — pipeline still completes with empty results."""
    clients = [
        FailingClient("claude"),
        FailingClient("openai"),
        FailingClient("gemini"),
    ]

    result = await run_pipeline(session_dir, depth=0, config=config_no_keys, clients=clients)

    assert result.providers_used == []
    assert len(result.providers_failed) == 3
    assert result.topics_identified == []
    # Structural files still written (empty)
    assert (session_dir / "comparison-matrix.md").exists()
    assert (session_dir / "validation-log.md").exists()


@pytest.mark.asyncio
async def test_citation_extraction_and_count(session_dir, config_no_keys):
    """Citations from markdown and ResearchResult.citations are collected and deduped."""
    md_citations = [Citation(text="A study", url="https://example.com/a", title="Study A")]
    clients = [
        FakeClient(
            "claude",
            "See [Study A](https://example.com/a) and [Study B](https://example.com/b).",
            citations=md_citations,
        ),
    ]

    result = await run_pipeline(session_dir, depth=0, config=config_no_keys, clients=clients)

    # example.com/a appears in both markdown and ResearchResult.citations, should dedup
    assert result.citation_count == 2  # /a deduped, /b unique


@pytest.mark.asyncio
async def test_depth_zero_no_validation(session_dir, config_no_keys):
    """At depth 0, no citations are validated."""
    clients = [
        FakeClient("claude", "See [Link](https://example.com/test)."),
    ]

    result = await run_pipeline(session_dir, depth=0, config=config_no_keys, clients=clients)

    assert result.citations_validated == 0


@pytest.mark.asyncio
async def test_missing_prompt_raises(tmp_path, config_no_keys):
    """Missing prompt.md raises FileNotFoundError."""
    sdir = tmp_path / "empty-session"
    sdir.mkdir()

    with pytest.raises(FileNotFoundError, match="prompt.md"):
        await run_pipeline(sdir, config=config_no_keys, clients=[])


@pytest.mark.asyncio
async def test_structural_outputs_content(session_dir, config_no_keys):
    """Verify comparison matrix and validation log have expected content."""
    clients = [
        FakeClient("claude", "## Security\nClaude security findings."),
        FakeClient("openai", "## Security\nOpenAI security findings.\n## Performance\nOpenAI perf."),
    ]

    await run_pipeline(session_dir, depth=0, config=config_no_keys, clients=clients)

    matrix_content = (session_dir / "comparison-matrix.md").read_text(encoding="utf-8")
    assert "Security" in matrix_content
    assert "Performance" in matrix_content

    val_log = (session_dir / "validation-log.md").read_text(encoding="utf-8")
    assert "Citation Validation Log" in val_log


def test_pipeline_result_model_dump():
    """PipelineResult.model_dump() returns correct structure."""
    pr = PipelineResult(
        session_dir="/tmp/test",
        providers_used=["claude", "openai"],
        providers_failed={"gemini": "API error"},
        citation_count=5,
        citations_validated=3,
        topics_identified=["Intro", "Methods"],
    )
    d = pr.model_dump()
    assert d["session_dir"] == "/tmp/test"
    assert d["providers_used"] == ["claude", "openai"]
    assert d["providers_failed"] == {"gemini": "API error"}
    assert d["citation_count"] == 5
    assert d["topics_identified"] == ["Intro", "Methods"]


@pytest.mark.asyncio
async def test_depth_one_validates_citations(session_dir, config_no_keys):
    """At depth 1, citations with URLs are validated (liveness check)."""
    clients = [
        FakeClient("claude", "See [Link](https://example.com/test)."),
    ]

    # Mock check_url_alive to return True without making real HTTP requests
    with patch(
        "giga_research.validation.citations.check_url_alive",
        new_callable=AsyncMock,
        return_value=True,
    ):
        result = await run_pipeline(session_dir, depth=1, config=config_no_keys, clients=clients)

    assert result.citations_validated > 0

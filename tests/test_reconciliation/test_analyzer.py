"""Tests for cross-report analysis."""

from __future__ import annotations

from giga_research.models import Citation, ResearchResult, ResultMetadata
from giga_research.reconciliation.analyzer import (
    build_comparison_matrix,
    deduplicate_citations,
    extract_citations_from_markdown,
)


def _make_result(provider: str, content: str) -> ResearchResult:
    return ResearchResult(
        provider=provider,
        content=content,
        citations=[],
        metadata=ResultMetadata(model="m", tokens_used=1, latency_s=0.1),
    )


def test_extract_citations_markdown_links():
    md = "According to [Source One](https://example.com/one), and also [Source Two](https://example.com/two)."
    citations = extract_citations_from_markdown(md)
    assert len(citations) == 2
    assert citations[0].title == "Source One"
    assert citations[0].url == "https://example.com/one"


def test_extract_citations_bare_urls():
    md = "See https://example.com/bare for details."
    citations = extract_citations_from_markdown(md)
    assert len(citations) >= 1
    assert any(c.url == "https://example.com/bare" for c in citations)


def test_extract_citations_no_links():
    md = "This text has no citations at all."
    citations = extract_citations_from_markdown(md)
    assert citations == []


def test_deduplicate_citations():
    c1 = Citation(text="claim A", url="https://example.com/1", title="Source 1")
    c2 = Citation(text="claim B", url="https://example.com/1", title="Source 1")
    c3 = Citation(text="claim C", url="https://example.com/2", title="Source 2")
    deduped = deduplicate_citations([c1, c2, c3])
    urls = [c.url for c in deduped]
    assert urls.count("https://example.com/1") == 1
    assert urls.count("https://example.com/2") == 1


def test_build_comparison_matrix():
    results = {
        "claude": _make_result("claude", "## Topic A\nClaude says X.\n## Topic B\nClaude says Y."),
        "openai": _make_result("openai", "## Topic A\nOpenAI says X.\n## Topic C\nOpenAI says Z."),
    }
    matrix = build_comparison_matrix(results)
    assert isinstance(matrix, dict)
    assert len(matrix) > 0

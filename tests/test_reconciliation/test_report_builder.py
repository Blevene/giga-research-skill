"""Tests for report builder output formatting."""

from __future__ import annotations

from giga_research.models import Citation, ValidationStatus
from giga_research.reconciliation.report_builder import (
    build_comparison_markdown,
    build_validation_log,
)


def test_build_comparison_markdown():
    matrix = {
        "Topic A": {"claude": "Claude's take on A", "openai": "OpenAI's take on A", "gemini": None},
        "Topic B": {"claude": None, "openai": "OpenAI on B", "gemini": "Gemini on B"},
    }
    md = build_comparison_markdown(matrix)
    assert "Topic A" in md
    assert "Topic B" in md
    assert "claude" in md.lower() or "Claude" in md
    assert "|" in md  # Should contain table formatting


def test_build_comparison_markdown_empty():
    md = build_comparison_markdown({})
    assert "No topics" in md or len(md) > 0


def test_build_validation_log_empty():
    log = build_validation_log([])
    assert "No citations" in log or len(log) > 0


def test_build_validation_log_with_results():
    citations = [
        Citation(text="Claim A", url="https://a.com", validation_status=ValidationStatus.VERIFIED),
        Citation(text="Claim B", url="https://b.com", validation_status=ValidationStatus.DEAD),
        Citation(text="Claim C", url="https://c.com", validation_status=ValidationStatus.HALLUCINATED),
    ]
    log = build_validation_log(citations)
    assert "VERIFIED" in log or "verified" in log
    assert "DEAD" in log or "dead" in log
    assert "HALLUCINATED" in log or "hallucinated" in log
    assert "https://a.com" in log

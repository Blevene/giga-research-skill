"""Tests for core Pydantic models."""

from __future__ import annotations

from giga_research.models import (
    Citation,
    ResearchResult,
    ResultMetadata,
    ValidationStatus,
)


def test_validation_status_values():
    assert ValidationStatus.UNCHECKED == "unchecked"
    assert ValidationStatus.ALIVE == "alive"
    assert ValidationStatus.DEAD == "dead"
    assert ValidationStatus.VERIFIED == "verified"
    assert ValidationStatus.HALLUCINATED == "hallucinated"
    assert ValidationStatus.REPLACED == "replaced"


def test_citation_defaults():
    c = Citation(text="Some claim")
    assert c.url is None
    assert c.title is None
    assert c.validation_status == ValidationStatus.UNCHECKED


def test_citation_with_all_fields():
    c = Citation(
        text="Claim text",
        url="https://example.com",
        title="Example",
        validation_status=ValidationStatus.VERIFIED,
    )
    assert c.url == "https://example.com"
    assert c.validation_status == ValidationStatus.VERIFIED


def test_result_metadata():
    m = ResultMetadata(
        model="claude-sonnet-4-5-20250929",
        tokens_used=1234,
        latency_s=12.5,
    )
    assert m.model == "claude-sonnet-4-5-20250929"
    assert m.tokens_used == 1234
    assert m.latency_s == 12.5


def test_research_result():
    r = ResearchResult(
        provider="claude",
        content="# Research\n\nSome findings.",
        citations=[Citation(text="A claim", url="https://example.com")],
        metadata=ResultMetadata(
            model="claude-sonnet-4-5-20250929",
            tokens_used=100,
            latency_s=1.0,
        ),
    )
    assert r.provider == "claude"
    assert len(r.citations) == 1
    assert r.citations[0].text == "A claim"


def test_research_result_empty_citations():
    r = ResearchResult(
        provider="openai",
        content="Content",
        citations=[],
        metadata=ResultMetadata(model="gpt-4o", tokens_used=50, latency_s=0.5),
    )
    assert r.citations == []

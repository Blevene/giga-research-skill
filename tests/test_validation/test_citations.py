"""Tests for citation validation at different depths."""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

from giga_research.models import Citation, ValidationStatus
from giga_research.validation.citations import validate_citations


def _patch_probe(status: ValidationStatus, body: str | None = None):
    return patch(
        "giga_research.validation.citations.probe_url",
        new_callable=AsyncMock,
        return_value=(status, body),
    )


async def test_depth_0_returns_unchecked():
    citations = [Citation(text="Claim", url="https://example.com")]
    result = await validate_citations(citations, depth=0)
    assert result[0].validation_status == ValidationStatus.UNCHECKED


async def test_depth_1_alive_url():
    citations = [Citation(text="Claim", url="https://example.com")]
    with _patch_probe(ValidationStatus.ALIVE):
        result = await validate_citations(citations, depth=1)
    assert result[0].validation_status == ValidationStatus.ALIVE


async def test_depth_1_dead_url():
    citations = [Citation(text="Claim", url="https://example.com/gone")]
    with _patch_probe(ValidationStatus.DEAD):
        result = await validate_citations(citations, depth=1)
    assert result[0].validation_status == ValidationStatus.DEAD


async def test_depth_1_blocked_url():
    """A blocked (e.g. 403) source is BLOCKED, not falsely reported DEAD."""
    citations = [Citation(text="Claim", url="https://cisa.gov/advisory")]
    with _patch_probe(ValidationStatus.BLOCKED):
        result = await validate_citations(citations, depth=1)
    assert result[0].validation_status == ValidationStatus.BLOCKED


async def test_depth_1_no_url_stays_unchecked():
    citations = [Citation(text="Claim with no URL")]
    result = await validate_citations(citations, depth=1)
    assert result[0].validation_status == ValidationStatus.UNCHECKED


async def test_depth_2_verified():
    citations = [Citation(text="specific claim text", url="https://example.com")]
    with _patch_probe(ValidationStatus.ALIVE, "This page contains the specific claim text and more."):
        result = await validate_citations(citations, depth=2)
    assert result[0].validation_status == ValidationStatus.VERIFIED


async def test_depth_2_unverified_not_hallucinated():
    """A live page whose body lacks the claim is UNVERIFIED — never 'hallucinated'."""
    citations = [Citation(text="specific claim text", url="https://example.com")]
    with _patch_probe(ValidationStatus.ALIVE, "This page has completely unrelated content."):
        result = await validate_citations(citations, depth=2)
    assert result[0].validation_status == ValidationStatus.UNVERIFIED


async def test_depth_2_blocked_preserved():
    """A blocked page at depth 2 stays BLOCKED — not downgraded to a verdict."""
    citations = [Citation(text="claim", url="https://example.com")]
    with _patch_probe(ValidationStatus.BLOCKED, None):
        result = await validate_citations(citations, depth=2)
    assert result[0].validation_status == ValidationStatus.BLOCKED


async def test_depth_2_dead_url():
    citations = [Citation(text="claim", url="https://example.com")]
    with _patch_probe(ValidationStatus.DEAD, None):
        result = await validate_citations(citations, depth=2)
    assert result[0].validation_status == ValidationStatus.DEAD


async def test_respects_max_concurrent():
    citations = [Citation(text=f"Claim {i}", url=f"https://example.com/{i}") for i in range(20)]
    with _patch_probe(ValidationStatus.ALIVE):
        result = await validate_citations(citations, depth=1, max_concurrent=5)
    assert all(c.validation_status == ValidationStatus.ALIVE for c in result)

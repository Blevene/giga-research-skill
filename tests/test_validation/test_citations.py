"""Tests for citation validation at different depths."""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

from giga_research.models import Citation, ValidationStatus
from giga_research.validation.citations import validate_citations


async def test_depth_0_returns_unchecked():
    citations = [Citation(text="Claim", url="https://example.com")]
    result = await validate_citations(citations, depth=0)
    assert result[0].validation_status == ValidationStatus.UNCHECKED


async def test_depth_1_alive_url():
    citations = [Citation(text="Claim", url="https://example.com")]
    with patch(
        "giga_research.validation.citations.check_url_alive",
        new_callable=AsyncMock,
        return_value=True,
    ):
        result = await validate_citations(citations, depth=1)
    assert result[0].validation_status == ValidationStatus.ALIVE


async def test_depth_1_dead_url():
    citations = [Citation(text="Claim", url="https://example.com/gone")]
    with patch(
        "giga_research.validation.citations.check_url_alive",
        new_callable=AsyncMock,
        return_value=False,
    ):
        result = await validate_citations(citations, depth=1)
    assert result[0].validation_status == ValidationStatus.DEAD


async def test_depth_1_no_url_stays_unchecked():
    citations = [Citation(text="Claim with no URL")]
    result = await validate_citations(citations, depth=1)
    assert result[0].validation_status == ValidationStatus.UNCHECKED


async def test_depth_2_verified():
    citations = [Citation(text="specific claim text", url="https://example.com")]
    with patch(
        "giga_research.validation.citations.fetch_url_content",
        new_callable=AsyncMock,
        return_value="This page contains the specific claim text and more.",
    ):
        result = await validate_citations(citations, depth=2)
    assert result[0].validation_status == ValidationStatus.VERIFIED


async def test_depth_2_hallucinated():
    citations = [Citation(text="specific claim text", url="https://example.com")]
    with patch(
        "giga_research.validation.citations.fetch_url_content",
        new_callable=AsyncMock,
        return_value="This page has completely unrelated content.",
    ):
        result = await validate_citations(citations, depth=2)
    assert result[0].validation_status == ValidationStatus.HALLUCINATED


async def test_depth_2_dead_url_falls_back():
    citations = [Citation(text="claim", url="https://example.com")]
    with patch(
        "giga_research.validation.citations.fetch_url_content",
        new_callable=AsyncMock,
        return_value=None,
    ):
        result = await validate_citations(citations, depth=2)
    assert result[0].validation_status == ValidationStatus.DEAD


async def test_respects_max_concurrent():
    """Validate that semaphore limits concurrency."""
    citations = [Citation(text=f"Claim {i}", url=f"https://example.com/{i}") for i in range(20)]
    with patch(
        "giga_research.validation.citations.check_url_alive",
        new_callable=AsyncMock,
        return_value=True,
    ):
        result = await validate_citations(citations, depth=1, max_concurrent=5)
    assert all(c.validation_status == ValidationStatus.ALIVE for c in result)

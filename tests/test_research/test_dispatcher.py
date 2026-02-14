"""Tests for parallel research dispatcher."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from giga_research.config import Config
from giga_research.errors import ProviderError
from giga_research.models import ResearchResult, ResultMetadata
from giga_research.research.dispatcher import dispatch_research


def _make_result(provider: str) -> ResearchResult:
    return ResearchResult(
        provider=provider,
        content=f"Report from {provider}",
        citations=[],
        metadata=ResultMetadata(model=f"{provider}-model", tokens_used=100, latency_s=1.0),
    )


def _make_client(provider: str, *, fail: bool = False):
    client = MagicMock()
    client.provider_name = provider
    client.is_available.return_value = True
    if fail:
        client.research = AsyncMock(side_effect=ProviderError(provider, "API error"))
    else:
        client.research = AsyncMock(return_value=_make_result(provider))
    return client


async def test_dispatch_all_succeed():
    clients = [_make_client("claude"), _make_client("openai"), _make_client("gemini")]
    results, errors = await dispatch_research("prompt", clients)
    assert len(results) == 3
    assert len(errors) == 0
    assert "claude" in results
    assert results["claude"].content == "Report from claude"


async def test_dispatch_one_fails():
    clients = [_make_client("claude"), _make_client("openai", fail=True)]
    results, errors = await dispatch_research("prompt", clients)
    assert len(results) == 1
    assert "claude" in results
    assert len(errors) == 1
    assert "openai" in errors


async def test_dispatch_empty_clients():
    results, errors = await dispatch_research("prompt", [])
    assert results == {}
    assert errors == {}


async def test_dispatch_all_fail():
    clients = [_make_client("claude", fail=True), _make_client("openai", fail=True)]
    results, errors = await dispatch_research("prompt", clients)
    assert len(results) == 0
    assert len(errors) == 2

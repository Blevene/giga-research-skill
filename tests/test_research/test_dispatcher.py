"""Tests for parallel research dispatcher."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

from giga_research.errors import ProviderError
from giga_research.models import ResearchResult, ResultMetadata
from giga_research.research.dispatcher import dispatch_research
from giga_research.research.progress import ProviderCompleted, ProviderFailed, ProviderStarted


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


async def test_on_result_called_per_provider():
    clients = [_make_client("claude"), _make_client("openai")]
    collected: list[ResearchResult] = []
    await dispatch_research("prompt", clients, on_result=collected.append)
    assert len(collected) == 2
    providers = {r.provider for r in collected}
    assert providers == {"claude", "openai"}


async def test_on_progress_emits_started_and_completed():
    clients = [_make_client("claude"), _make_client("openai")]
    events: list = []
    await dispatch_research("prompt", clients, on_progress=events.append)
    started = [e for e in events if isinstance(e, ProviderStarted)]
    completed = [e for e in events if isinstance(e, ProviderCompleted)]
    assert len(started) == 2
    assert len(completed) == 2
    assert {e.provider for e in started} == {"claude", "openai"}
    assert {e.provider for e in completed} == {"claude", "openai"}
    for e in completed:
        assert e.latency_s >= 0


async def test_on_progress_emits_failed_for_error():
    clients = [_make_client("claude", fail=True)]
    events: list = []
    await dispatch_research("prompt", clients, on_progress=events.append)
    started = [e for e in events if isinstance(e, ProviderStarted)]
    failed = [e for e in events if isinstance(e, ProviderFailed)]
    assert len(started) == 1
    assert len(failed) == 1
    assert failed[0].provider == "claude"
    assert isinstance(failed[0].error, ProviderError)


async def test_on_result_not_called_for_failed_provider():
    clients = [_make_client("claude"), _make_client("openai", fail=True)]
    collected: list[ResearchResult] = []
    await dispatch_research("prompt", clients, on_result=collected.append)
    assert len(collected) == 1
    assert collected[0].provider == "claude"

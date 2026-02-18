"""Parallel research dispatch across providers."""

from __future__ import annotations

import asyncio
import time
from collections.abc import Callable

from giga_research.clients.base import BaseResearchClient
from giga_research.models import ResearchResult
from giga_research.research.progress import (
    ProgressCallback,
    ProviderCompleted,
    ProviderFailed,
    ProviderStarted,
)


async def dispatch_research(
    prompt: str,
    clients: list[BaseResearchClient],
    *,
    on_result: Callable[[ResearchResult], None] | None = None,
    on_progress: ProgressCallback | None = None,
) -> tuple[dict[str, ResearchResult], dict[str, Exception]]:
    """Dispatch research to all clients concurrently.

    Args:
        prompt: The research prompt.
        clients: List of provider clients to query.
        on_result: Called immediately when a provider succeeds (before others finish).
        on_progress: Called with ProgressEvent as providers start/complete/fail.

    Returns:
        Tuple of (successful results dict, error dict) keyed by provider name.
        One provider failing does not affect others.
    """
    if not clients:
        return {}, {}

    async def _run_one(client: BaseResearchClient) -> tuple[str, ResearchResult | Exception]:
        if on_progress:
            on_progress(ProviderStarted(provider=client.provider_name))
        t0 = time.monotonic()
        try:
            result = await client.research(prompt)
            elapsed = time.monotonic() - t0
            if on_progress:
                on_progress(ProviderCompleted(provider=client.provider_name, latency_s=elapsed))
            return (client.provider_name, result)
        except Exception as exc:
            if on_progress:
                on_progress(ProviderFailed(provider=client.provider_name, error=exc))
            return (client.provider_name, exc)

    tasks = [asyncio.create_task(_run_one(c)) for c in clients]

    results: dict[str, ResearchResult] = {}
    errors: dict[str, Exception] = {}

    for coro in asyncio.as_completed(tasks):
        provider_name, outcome = await coro
        if isinstance(outcome, Exception):
            errors[provider_name] = outcome
        else:
            results[provider_name] = outcome
            if on_result:
                on_result(outcome)

    return results, errors

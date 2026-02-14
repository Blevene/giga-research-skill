"""Parallel research dispatch across providers."""

from __future__ import annotations

import asyncio

from giga_research.clients.base import BaseResearchClient
from giga_research.models import ResearchResult


async def dispatch_research(
    prompt: str,
    clients: list[BaseResearchClient],
) -> tuple[dict[str, ResearchResult], dict[str, Exception]]:
    """Dispatch research to all clients concurrently.

    Returns:
        Tuple of (successful results dict, error dict) keyed by provider name.
        One provider failing does not affect others.
    """
    if not clients:
        return {}, {}

    async def _run_one(client: BaseResearchClient) -> tuple[str, ResearchResult | Exception]:
        try:
            result = await client.research(prompt)
            return (client.provider_name, result)
        except Exception as exc:
            return (client.provider_name, exc)

    outcomes = await asyncio.gather(*[_run_one(c) for c in clients])

    results: dict[str, ResearchResult] = {}
    errors: dict[str, Exception] = {}

    for provider_name, outcome in outcomes:
        if isinstance(outcome, Exception):
            errors[provider_name] = outcome
        else:
            results[provider_name] = outcome

    return results, errors

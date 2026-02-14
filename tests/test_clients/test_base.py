"""Tests for base client retry and timeout logic."""

from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock

import pytest

from giga_research.clients.base import BaseResearchClient
from giga_research.config import Config
from giga_research.errors import ProviderError, ProviderTimeoutError
from giga_research.models import ResearchResult, ResultMetadata


class FakeClient(BaseResearchClient):
    """Concrete test implementation of BaseResearchClient."""

    provider_name = "fake"

    def __init__(self, config: Config, call_fn: AsyncMock | None = None) -> None:
        super().__init__(config)
        self._call_fn = call_fn or AsyncMock(
            return_value=ResearchResult(
                provider="fake",
                content="result",
                citations=[],
                metadata=ResultMetadata(model="fake-1", tokens_used=10, latency_s=0.1),
            )
        )

    async def _do_research(self, prompt: str) -> ResearchResult:
        return await self._call_fn(prompt)

    def is_available(self) -> bool:
        return True


@pytest.fixture
def config() -> Config:
    return Config(max_retries=2, request_timeout=5)


async def test_research_calls_do_research(config: Config):
    client = FakeClient(config)
    result = await client.research("test prompt")
    assert result.provider == "fake"
    client._call_fn.assert_awaited_once_with("test prompt")


async def test_research_retries_on_provider_error(config: Config):
    call_fn = AsyncMock(
        side_effect=[
            ProviderError("fake", "transient failure"),
            ResearchResult(
                provider="fake",
                content="ok",
                citations=[],
                metadata=ResultMetadata(model="fake-1", tokens_used=10, latency_s=0.1),
            ),
        ]
    )
    client = FakeClient(config, call_fn)
    result = await client.research("test")
    assert result.content == "ok"
    assert call_fn.await_count == 2


async def test_research_raises_after_max_retries(config: Config):
    call_fn = AsyncMock(side_effect=ProviderError("fake", "always fails"))
    client = FakeClient(config, call_fn)
    with pytest.raises(ProviderError, match="always fails"):
        await client.research("test")
    assert call_fn.await_count == 3  # initial + 2 retries


async def test_research_timeout(config: Config):
    async def slow_call(prompt: str) -> ResearchResult:
        await asyncio.sleep(100)
        raise AssertionError("Should not reach here")

    client = FakeClient(Config(max_retries=0, request_timeout=1))
    client._call_fn = slow_call  # type: ignore[assignment]
    with pytest.raises(ProviderTimeoutError):
        await client.research("test")

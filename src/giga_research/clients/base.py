"""Abstract base client with retry, timeout, and backoff."""

from __future__ import annotations

import asyncio
import random
from abc import ABC, abstractmethod

from giga_research.config import Config
from giga_research.errors import ProviderError, ProviderTimeoutError
from giga_research.models import ResearchResult


class BaseResearchClient(ABC):
    """Base class for research provider clients.

    Provides retry with exponential backoff + jitter, and timeout guards.
    Subclasses implement _do_research() with provider-specific logic.
    """

    provider_name: str = ""

    def __init__(self, config: Config) -> None:
        self.config = config

    async def research(self, prompt: str) -> ResearchResult:
        """Execute research with retry and timeout."""
        last_error: Exception | None = None

        for attempt in range(self.config.max_retries + 1):
            try:
                return await asyncio.wait_for(
                    self._do_research(prompt),
                    timeout=self.config.request_timeout,
                )
            except asyncio.TimeoutError:
                raise ProviderTimeoutError(
                    self.provider_name, self.config.request_timeout
                )
            except ProviderError as exc:
                last_error = exc
                if attempt < self.config.max_retries:
                    delay = (2**attempt) + random.uniform(0, 1)
                    await asyncio.sleep(delay)

        raise last_error  # type: ignore[misc]

    @abstractmethod
    async def _do_research(self, prompt: str) -> ResearchResult:
        """Provider-specific research implementation."""

    @abstractmethod
    def is_available(self) -> bool:
        """Check if this provider has a configured API key."""

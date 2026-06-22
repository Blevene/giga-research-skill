"""Abstract base client with retry, timeout, and backoff."""

from __future__ import annotations

import asyncio
import random
from abc import ABC, abstractmethod

from giga_research.config import Config
from giga_research.errors import ProviderError, ProviderRateLimitError, ProviderTimeoutError
from giga_research.models import ResearchResult

# Rate limits (esp. per-minute token limits) need a real wait, not the 1-5s
# exponential backoff used for generic provider errors.
_RATE_LIMIT_BASE_DELAY = 20.0
_RATE_LIMIT_MAX_DELAY = 90.0


class BaseResearchClient(ABC):
    """Base class for research provider clients.

    Provides retry with exponential backoff + jitter, and timeout guards.
    Subclasses implement _do_research() with provider-specific logic.
    """

    provider_name: str = ""
    # Subclasses can override to set a provider-specific timeout (seconds).
    # When set, this takes precedence over config.request_timeout.
    default_timeout: int | None = None

    def __init__(self, config: Config) -> None:
        self.config = config

    @property
    def timeout(self) -> int:
        """Effective timeout: provider-specific override or global config."""
        return self.default_timeout if self.default_timeout is not None else self.config.request_timeout

    async def research(self, prompt: str) -> ResearchResult:
        """Execute research with retry and timeout."""
        last_error: Exception | None = None

        for attempt in range(self.config.max_retries + 1):
            try:
                return await asyncio.wait_for(
                    self._do_research(prompt),
                    timeout=self.timeout,
                )
            except TimeoutError as exc:
                raise ProviderTimeoutError(self.provider_name, self.timeout) from exc
            except ProviderError as exc:
                last_error = exc
                if attempt < self.config.max_retries:
                    if isinstance(exc, ProviderRateLimitError):
                        # Honor a server-provided retry-after, else back off long
                        # enough for a per-minute window to clear.
                        delay = exc.retry_after_s if exc.retry_after_s is not None else min(
                            _RATE_LIMIT_BASE_DELAY * (2**attempt), _RATE_LIMIT_MAX_DELAY
                        )
                    else:
                        delay = (2**attempt) + random.uniform(0, 1)
                    await asyncio.sleep(delay)

        raise last_error  # type: ignore[misc]

    @abstractmethod
    async def _do_research(self, prompt: str) -> ResearchResult:
        """Provider-specific research implementation."""

    @abstractmethod
    def is_available(self) -> bool:
        """Check if this provider has a configured API key."""

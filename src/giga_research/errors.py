"""Structured error types for giga_research."""

from __future__ import annotations


class GigaResearchError(Exception):
    """Base error for all giga_research exceptions."""


class ProviderError(GigaResearchError):
    """Error from a research provider API."""

    def __init__(self, provider: str, message: str) -> None:
        self.provider = provider
        super().__init__(f"[{provider}] {message}")


class ProviderTimeoutError(ProviderError):
    """Provider request timed out."""

    def __init__(self, provider: str, timeout_s: int) -> None:
        self.timeout_s = timeout_s
        super().__init__(provider, f"Request timed out after {timeout_s}s")


class ProviderRateLimitError(ProviderError):
    """Provider returned a rate limit response."""

    def __init__(self, provider: str, retry_after_s: float | None = None) -> None:
        self.retry_after_s = retry_after_s
        msg = "Rate limited"
        if retry_after_s is not None:
            msg += f", retry after {retry_after_s}s"
        super().__init__(provider, msg)


class ValidationError(GigaResearchError):
    """Error during citation validation."""

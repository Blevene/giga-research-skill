"""Structured error types for giga_research."""

from __future__ import annotations

import re

_RATE_LIMIT_MARKERS = (
    "rate limit",
    "rate_limit",
    "ratelimit",
    "429",
    "too many requests",
    "tokens per min",
    "tpm",
    "quota",
)


def is_rate_limit_message(message: str) -> bool:
    """True if a provider error message indicates a (retryable) rate limit."""
    lowered = message.lower()
    return any(marker in lowered for marker in _RATE_LIMIT_MARKERS)


def parse_retry_after_seconds(message: str) -> float | None:
    """Extract a retry-after delay from messages like 'try again in 1.5s'."""
    match = re.search(
        r"(?:try again in|retry after|retry-after:?)\s+([\d.]+)\s*"
        r"(ms|s|sec|secs|seconds|m|min|mins|minutes)?",
        message,
        re.IGNORECASE,
    )
    if not match:
        return None
    value = float(match.group(1))
    unit = (match.group(2) or "s").lower()
    if unit == "ms":
        return value / 1000
    if unit.startswith("m") and unit != "ms":
        return value * 60
    return value


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

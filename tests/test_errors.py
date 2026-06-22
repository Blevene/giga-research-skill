"""Tests for structured error types."""

from __future__ import annotations

import pytest

from giga_research.errors import (
    GigaResearchError,
    ProviderError,
    ProviderRateLimitError,
    ProviderTimeoutError,
    ValidationError,
    is_rate_limit_message,
    parse_retry_after_seconds,
)


def test_base_error():
    err = GigaResearchError("something failed")
    assert str(err) == "something failed"
    assert isinstance(err, Exception)


def test_provider_error():
    err = ProviderError("claude", "API returned 500")
    assert err.provider == "claude"
    assert "claude" in str(err)
    assert "500" in str(err)


def test_provider_timeout():
    err = ProviderTimeoutError("openai", timeout_s=300)
    assert err.provider == "openai"
    assert err.timeout_s == 300
    assert isinstance(err, ProviderError)


def test_provider_rate_limit():
    err = ProviderRateLimitError("gemini", retry_after_s=60.0)
    assert err.retry_after_s == 60.0
    assert isinstance(err, ProviderError)


def test_validation_error():
    err = ValidationError("Invalid citation URL")
    assert isinstance(err, GigaResearchError)


@pytest.mark.parametrize(
    "message",
    [
        "Rate limit reached for gpt-5.5-pro on tokens per min (TPM): Limit 1000000",
        "Error code: 429 - too many requests",
        "You exceeded your current quota",
        "RateLimitError: slow down",
    ],
)
def test_is_rate_limit_message_true(message: str):
    assert is_rate_limit_message(message) is True


@pytest.mark.parametrize(
    "message",
    ["Deep research failed: internal server error", "invalid request", "budget_exceeded"],
)
def test_is_rate_limit_message_false(message: str):
    assert is_rate_limit_message(message) is False


@pytest.mark.parametrize(
    ("message", "expected"),
    [
        ("Rate limited; try again in 1.5s", 1.5),
        ("Please retry after 30 seconds", 30.0),
        ("try again in 200ms", 0.2),
        ("try again in 2 minutes", 120.0),
        ("rate limit reached", None),
    ],
)
def test_parse_retry_after_seconds(message: str, expected: float | None):
    assert parse_retry_after_seconds(message) == expected

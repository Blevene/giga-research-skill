"""Tests for structured error types."""

from __future__ import annotations

from giga_research.errors import (
    GigaResearchError,
    ProviderError,
    ProviderRateLimitError,
    ProviderTimeoutError,
    ValidationError,
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

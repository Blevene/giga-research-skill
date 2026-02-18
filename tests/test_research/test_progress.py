"""Tests for progress event dataclasses."""

from __future__ import annotations

import dataclasses

import pytest

from giga_research.research.progress import (
    ProgressEvent,
    ProviderCompleted,
    ProviderFailed,
    ProviderStarted,
)


def test_provider_started_fields():
    event = ProviderStarted(provider="claude")
    assert event.provider == "claude"


def test_provider_completed_fields():
    event = ProviderCompleted(provider="openai", latency_s=12.5)
    assert event.provider == "openai"
    assert event.latency_s == 12.5


def test_provider_failed_fields():
    err = RuntimeError("boom")
    event = ProviderFailed(provider="gemini", error=err)
    assert event.provider == "gemini"
    assert event.error is err


def test_events_are_frozen():
    event = ProviderStarted(provider="claude")
    with pytest.raises(dataclasses.FrozenInstanceError):
        event.provider = "openai"  # type: ignore[misc]


def test_progress_event_union_accepts_all_types():
    events: list[ProgressEvent] = [
        ProviderStarted(provider="a"),
        ProviderCompleted(provider="b", latency_s=1.0),
        ProviderFailed(provider="c", error=ValueError("x")),
    ]
    assert len(events) == 3

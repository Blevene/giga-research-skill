"""Progress events emitted during research dispatch."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Union


@dataclass(frozen=True)
class ProviderStarted:
    """Emitted when a provider coroutine begins."""

    provider: str


@dataclass(frozen=True)
class ProviderCompleted:
    """Emitted when a provider succeeds."""

    provider: str
    latency_s: float


@dataclass(frozen=True)
class ProviderFailed:
    """Emitted when a provider raises an exception."""

    provider: str
    error: Exception


ProgressEvent = Union[ProviderStarted, ProviderCompleted, ProviderFailed]
ProgressCallback = Callable[[ProgressEvent], None]

"""Core data models for giga_research."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel


class ValidationStatus(StrEnum):
    """Status of a citation after validation."""

    UNCHECKED = "unchecked"
    ALIVE = "alive"
    DEAD = "dead"
    VERIFIED = "verified"
    HALLUCINATED = "hallucinated"
    REPLACED = "replaced"


class Citation(BaseModel):
    """A citation extracted from a research report."""

    text: str
    url: str | None = None
    title: str | None = None
    validation_status: ValidationStatus = ValidationStatus.UNCHECKED
    replacement_url: str | None = None


class ResultMetadata(BaseModel):
    """Metadata about a provider's research response."""

    model: str
    tokens_used: int
    latency_s: float


class ResearchResult(BaseModel):
    """Normalized result from a research provider."""

    provider: str
    content: str
    citations: list[Citation]
    metadata: ResultMetadata

"""Core data models for giga_research."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel


class ValidationStatus(StrEnum):
    """Status of a citation after validation."""

    UNCHECKED = "unchecked"
    ALIVE = "alive"
    DEAD = "dead"  # genuinely gone/fabricated: 404/410, unresolvable host, invalid URL
    BLOCKED = "blocked"  # exists but unreadable: 401/403/405/429, anti-bot, timeout
    VERIFIED = "verified"  # depth 2: live page whose text supports the claim
    UNVERIFIED = "unverified"  # depth 2: live page, claim not found (paraphrase/JS/absent — not an accusation)
    HALLUCINATED = "hallucinated"  # retained for back-compat; no longer emitted by the validator
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

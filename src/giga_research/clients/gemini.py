"""Gemini (Google) deep research client using the Interactions API."""

from __future__ import annotations

import asyncio
import time

from google import genai

from giga_research.clients.base import BaseResearchClient
from giga_research.config import Config
from giga_research.errors import ProviderError
from giga_research.models import Citation, ResearchResult, ResultMetadata

_AGENT = "deep-research-preview-04-2026"
_POLL_INTERVAL_S = 10

# Terminal statuses that are not a successful completion. The Interactions API
# status enum grew beyond completed/failed (Api-Revision 2026-05-20): a run can
# also be cancelled, exhaust its token budget, or stop incomplete.
_FAILURE_STATUSES = frozenset({"failed", "cancelled", "budget_exceeded", "incomplete"})


class GeminiClient(BaseResearchClient):
    """Research client using Gemini Deep Research via the Interactions API."""

    provider_name = "gemini"
    default_timeout = 1800  # 30 minutes — deep research is long-running

    def __init__(self, config: Config) -> None:
        super().__init__(config)
        if config.gemini_api_key:
            self._client = genai.Client(api_key=config.gemini_api_key)
        else:
            self._client = None

    def is_available(self) -> bool:
        return self._client is not None

    async def _do_research(self, prompt: str) -> ResearchResult:
        if self._client is None:
            raise ProviderError("gemini", "No API key configured")

        start = time.monotonic()
        try:
            # Launch deep research as a background interaction
            interaction = self._client.interactions.create(
                input=prompt,
                agent=_AGENT,
                background=True,
            )

            # Poll until a terminal status
            while True:
                interaction = self._client.interactions.get(interaction.id)
                status = getattr(interaction, "status", None)
                if status == "completed":
                    break
                if status in _FAILURE_STATUSES:
                    error_msg = getattr(interaction, "error", None) or status
                    raise ProviderError("gemini", f"Deep research {status}: {error_msg}")
                await asyncio.sleep(_POLL_INTERVAL_S)

        except ProviderError:
            raise
        except Exception as exc:
            raise ProviderError("gemini", str(exc)) from exc

        latency = time.monotonic() - start

        content, citations = _extract_content_and_citations(interaction)
        tokens = _extract_tokens(interaction)

        return ResearchResult(
            provider="gemini",
            content=content,
            citations=citations,
            metadata=ResultMetadata(
                model=getattr(interaction, "model", None) or _AGENT,
                tokens_used=tokens,
                latency_s=round(latency, 2),
            ),
        )


def _extract_content_and_citations(interaction: object) -> tuple[str, list[Citation]]:
    """Pull report text and source citations from an interaction.

    Version-defensive across the google-genai schema change: 2.x exposes the
    convenience ``output_text`` plus a ``steps`` array, while 1.x used an
    ``outputs`` array of items. Either way, citations live as ``annotations``
    on text content blocks.
    """
    seen_urls: set[str] = set()
    citations: list[Citation] = []
    text_parts: list[str] = []

    # Content-bearing items: 2.x `steps`, else 1.x `outputs`.
    items = getattr(interaction, "steps", None)
    if not items:
        items = getattr(interaction, "outputs", None) or []

    for item in items:
        blocks = getattr(item, "content", None)
        if blocks is None:
            # 1.x output items may expose `.text` directly.
            item_text = getattr(item, "text", None)
            if item_text:
                text_parts.append(item_text)
            continue
        for block in blocks:
            block_text = getattr(block, "text", None)
            if block_text:
                text_parts.append(block_text)
            for ann in getattr(block, "annotations", None) or []:
                citation = _annotation_to_citation(ann, seen_urls)
                if citation is not None:
                    citations.append(citation)

    # Prefer the SDK's joined convenience property when available and non-empty.
    output_text = getattr(interaction, "output_text", None)
    content = output_text if isinstance(output_text, str) and output_text else "\n\n".join(text_parts)

    return content, citations


def _annotation_to_citation(ann: object, seen_urls: set[str]) -> Citation | None:
    """Convert a text annotation to a Citation, deduplicating by URL.

    Newer schemas put `url`/`title` directly on the annotation; older ones wrap
    them in a `source` object.
    """
    url = getattr(ann, "url", None)
    title = getattr(ann, "title", None)
    source = getattr(ann, "source", None)
    if source is not None:
        url = url or getattr(source, "url", None)
        title = title or getattr(source, "title", None)
    if not url or url in seen_urls:
        return None
    seen_urls.add(url)
    return Citation(
        text=getattr(ann, "cited_text", None) or title or "",
        url=url,
        title=title,
    )


def _extract_tokens(interaction: object) -> int:
    """Best-effort total token count from interaction.usage across schema versions."""
    usage = getattr(interaction, "usage", None)
    if usage is None:
        return 0
    total = getattr(usage, "total_tokens", None)
    if isinstance(total, int):
        return total
    inp = getattr(usage, "total_input_tokens", None) or getattr(usage, "input_tokens", None) or 0
    out = getattr(usage, "total_output_tokens", None) or getattr(usage, "output_tokens", None) or 0
    return (inp or 0) + (out or 0)

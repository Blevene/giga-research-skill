"""Gemini (Google) deep research client using the Interactions API."""

from __future__ import annotations

import asyncio
import time

from google import genai

from giga_research.clients.base import BaseResearchClient
from giga_research.config import DEFAULT_GEMINI_AGENT, Config
from giga_research.errors import (
    ProviderError,
    ProviderRateLimitError,
    is_rate_limit_message,
    parse_retry_after_seconds,
)
from giga_research.models import Citation, ResearchResult, ResultMetadata

# Default agent; overridable via GEMINI_RESEARCH_AGENT.
_AGENT = DEFAULT_GEMINI_AGENT
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
        self._agent = config.gemini_agent
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
                agent=self._agent,
                background=True,
            )

            # Poll until a terminal status
            while True:
                interaction = self._client.interactions.get(interaction.id)
                status = getattr(interaction, "status", None)
                if status == "completed":
                    break
                if status in _FAILURE_STATUSES:
                    error_msg = str(getattr(interaction, "error", None) or status)
                    if is_rate_limit_message(error_msg):
                        raise ProviderRateLimitError("gemini", parse_retry_after_seconds(error_msg))
                    raise ProviderError("gemini", f"Deep research {status}: {error_msg}")
                await asyncio.sleep(_POLL_INTERVAL_S)

        except ProviderError:
            raise
        except Exception as exc:
            if is_rate_limit_message(str(exc)):
                raise ProviderRateLimitError("gemini", parse_retry_after_seconds(str(exc))) from exc
            raise ProviderError("gemini", str(exc)) from exc

        latency = time.monotonic() - start

        content, citations = _extract_content_and_citations(interaction)
        tokens = _extract_tokens(interaction)

        return ResearchResult(
            provider="gemini",
            content=content,
            citations=citations,
            metadata=ResultMetadata(
                model=getattr(interaction, "model", None) or self._agent,
                tokens_used=tokens,
                latency_s=round(latency, 2),
            ),
        )


def _extract_content_and_citations(interaction: object) -> tuple[str, list[Citation]]:
    """Pull the full report text and source citations from an interaction.

    The report is assembled from the ``model_output`` steps (2.x schema). We do
    NOT use ``interaction.output_text`` for the body: it returns only the final
    output segment, so a multi-step report loses its leading sections (title,
    intro, and earlier topics). Citations live as ``annotations`` on text blocks.

    Version-defensive: falls back to the 1.x ``outputs`` array, and finally to
    ``output_text`` only if no step text is found at all.
    """
    seen_urls: set[str] = set()
    citations: list[Citation] = []
    text_parts: list[str] = []

    steps = getattr(interaction, "steps", None)
    if steps:
        for step in steps:
            # Skip the echoed user input and any tool/thinking steps — keep the report.
            if getattr(step, "type", None) != "model_output":
                continue
            for block in getattr(step, "content", None) or []:
                block_text = getattr(block, "text", None)
                if block_text:
                    text_parts.append(block_text)
                for ann in getattr(block, "annotations", None) or []:
                    citation = _annotation_to_citation(ann, seen_urls)
                    if citation is not None:
                        citations.append(citation)
        # Each model_output text block carries its own leading/trailing newlines.
        content = "".join(text_parts)
    else:
        # 1.x fallback: an `outputs` array of items, each with `.content` blocks
        # or a direct `.text`.
        for item in getattr(interaction, "outputs", None) or []:
            blocks = getattr(item, "content", None)
            if blocks is None:
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
        content = "\n\n".join(text_parts)

    # Last resort only: if no step/output text was found, use output_text.
    if not content.strip():
        output_text = getattr(interaction, "output_text", None)
        if isinstance(output_text, str):
            content = output_text

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

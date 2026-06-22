"""OpenAI deep research client using the Responses API."""

from __future__ import annotations

import asyncio
import time

from openai import AsyncOpenAI

from giga_research.clients.base import BaseResearchClient
from giga_research.config import DEFAULT_OPENAI_MODEL, Config
from giga_research.errors import (
    ProviderError,
    ProviderRateLimitError,
    is_rate_limit_message,
    parse_retry_after_seconds,
)
from giga_research.models import Citation, ResearchResult, ResultMetadata

# Default is the dedicated, proven deep-research model. o4-mini-deep-research
# (cheaper/faster) and gpt-5.5-pro (general successor; o3/o4-mini deep-research
# retire 2026-12-11) can be selected via OPENAI_RESEARCH_MODEL.
_MODEL = DEFAULT_OPENAI_MODEL
_POLL_INTERVAL_S = 10


class OpenAIClient(BaseResearchClient):
    """Research client using OpenAI Deep Research via the Responses API."""

    provider_name = "openai"
    default_timeout = 1800  # 30 minutes — deep research is long-running

    def __init__(self, config: Config) -> None:
        super().__init__(config)
        self._model = config.openai_model
        if config.openai_api_key:
            self._client = AsyncOpenAI(api_key=config.openai_api_key, timeout=3600)
        else:
            self._client = None

    def is_available(self) -> bool:
        return self._client is not None

    async def _do_research(self, prompt: str) -> ResearchResult:
        if self._client is None:
            raise ProviderError("openai", "No API key configured")

        start = time.monotonic()
        try:
            # Launch deep research as a background response
            response = await self._client.responses.create(
                model=self._model,
                input=prompt,
                background=True,
                tools=[{"type": "web_search"}],
                instructions=(
                    "You are a thorough research assistant. Provide comprehensive, "
                    "well-cited research with clear structure and evidence-based findings."
                ),
            )

            # Poll until completion
            while response.status not in ("completed", "failed"):
                await asyncio.sleep(_POLL_INTERVAL_S)
                response = await self._client.responses.retrieve(response.id)

            if response.status == "failed":
                error_msg = getattr(getattr(response, "error", None), "message", "Unknown error")
                if is_rate_limit_message(error_msg):
                    raise ProviderRateLimitError("openai", parse_retry_after_seconds(error_msg))
                raise ProviderError("openai", f"Deep research failed: {error_msg}")

        except ProviderError:
            raise
        except Exception as exc:
            if is_rate_limit_message(str(exc)):
                raise ProviderRateLimitError("openai", parse_retry_after_seconds(str(exc))) from exc
            raise ProviderError("openai", str(exc)) from exc

        latency = time.monotonic() - start
        content = response.output_text or ""
        citations = _extract_citations(response)
        tokens = 0
        if response.usage:
            tokens = (response.usage.input_tokens or 0) + (response.usage.output_tokens or 0)

        return ResearchResult(
            provider="openai",
            content=content,
            citations=citations,
            metadata=ResultMetadata(
                model=response.model or self._model,
                tokens_used=tokens,
                latency_s=round(latency, 2),
            ),
        )


def _extract_citations(response: object) -> list[Citation]:
    """Extract url-citation annotations from Responses API output text blocks.

    Each output message holds content blocks; output-text blocks carry an
    `annotations` list of url citations (`url`, `title`, `start_index`,
    `end_index`). Deduplicated by URL.
    """
    seen_urls: set[str] = set()
    citations: list[Citation] = []

    for item in getattr(response, "output", None) or []:
        for block in getattr(item, "content", None) or []:
            for ann in getattr(block, "annotations", None) or []:
                url = getattr(ann, "url", None)
                if not url or url in seen_urls:
                    continue
                seen_urls.add(url)
                title = getattr(ann, "title", None)
                citations.append(Citation(text=title or "", url=url, title=title))

    return citations

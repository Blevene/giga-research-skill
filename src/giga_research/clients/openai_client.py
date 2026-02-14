"""OpenAI deep research client using the Responses API."""

from __future__ import annotations

import asyncio
import time

from openai import AsyncOpenAI

from giga_research.clients.base import BaseResearchClient
from giga_research.config import Config
from giga_research.errors import ProviderError
from giga_research.models import ResearchResult, ResultMetadata

_MODEL = "o3-deep-research"
_POLL_INTERVAL_S = 10


class OpenAIClient(BaseResearchClient):
    """Research client using OpenAI Deep Research via the Responses API."""

    provider_name = "openai"
    default_timeout = 1800  # 30 minutes — deep research is long-running

    def __init__(self, config: Config) -> None:
        super().__init__(config)
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
                model=_MODEL,
                input=prompt,
                background=True,
                tools=[{"type": "web_search_preview"}],
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
                raise ProviderError("openai", f"Deep research failed: {error_msg}")

        except ProviderError:
            raise
        except Exception as exc:
            raise ProviderError("openai", str(exc)) from exc

        latency = time.monotonic() - start
        content = response.output_text or ""
        tokens = 0
        if response.usage:
            tokens = (response.usage.input_tokens or 0) + (response.usage.output_tokens or 0)

        return ResearchResult(
            provider="openai",
            content=content,
            citations=[],
            metadata=ResultMetadata(
                model=response.model or _MODEL,
                tokens_used=tokens,
                latency_s=round(latency, 2),
            ),
        )

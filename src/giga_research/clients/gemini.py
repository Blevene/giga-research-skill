"""Gemini (Google) deep research client using the Interactions API."""

from __future__ import annotations

import asyncio
import time

from google import genai

from giga_research.clients.base import BaseResearchClient
from giga_research.config import Config
from giga_research.errors import ProviderError
from giga_research.models import ResearchResult, ResultMetadata

_AGENT = "deep-research-pro-preview-12-2025"
_POLL_INTERVAL_S = 10


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

            # Poll until completion
            while True:
                interaction = self._client.interactions.get(interaction.id)
                if interaction.status == "completed":
                    break
                elif interaction.status == "failed":
                    error_msg = getattr(interaction, "error", "Unknown error")
                    raise ProviderError("gemini", f"Deep research failed: {error_msg}")
                await asyncio.sleep(_POLL_INTERVAL_S)

        except ProviderError:
            raise
        except Exception as exc:
            raise ProviderError("gemini", str(exc)) from exc

        latency = time.monotonic() - start
        content = interaction.outputs[-1].text if interaction.outputs else ""

        return ResearchResult(
            provider="gemini",
            content=content,
            citations=[],
            metadata=ResultMetadata(
                model=_AGENT,
                tokens_used=0,  # Interactions API doesn't expose token counts directly
                latency_s=round(latency, 2),
            ),
        )

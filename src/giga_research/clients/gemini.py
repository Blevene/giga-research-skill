"""Gemini (Google) research client."""

from __future__ import annotations

import time

from google import genai

from giga_research.clients.base import BaseResearchClient
from giga_research.config import Config
from giga_research.errors import ProviderError
from giga_research.models import ResearchResult, ResultMetadata


class GeminiClient(BaseResearchClient):
    """Research client using the Google Gemini API."""

    provider_name = "gemini"

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
            response = await self._client.aio.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
                config=genai.types.GenerateContentConfig(
                    system_instruction="You are a thorough research assistant. Provide comprehensive, well-cited research with clear structure and evidence-based findings.",
                    max_output_tokens=16384,
                ),
            )
        except Exception as exc:
            raise ProviderError("gemini", str(exc)) from exc

        latency = time.monotonic() - start
        content = response.text or ""
        prompt_tokens = getattr(response.usage_metadata, "prompt_token_count", 0) or 0
        completion_tokens = getattr(response.usage_metadata, "candidates_token_count", 0) or 0

        return ResearchResult(
            provider="gemini",
            content=content,
            citations=[],
            metadata=ResultMetadata(
                model="gemini-2.0-flash",
                tokens_used=prompt_tokens + completion_tokens,
                latency_s=round(latency, 2),
            ),
        )

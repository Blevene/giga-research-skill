"""OpenAI research client."""

from __future__ import annotations

import time

from openai import AsyncOpenAI

from giga_research.clients.base import BaseResearchClient
from giga_research.config import Config
from giga_research.errors import ProviderError
from giga_research.models import ResearchResult, ResultMetadata


class OpenAIClient(BaseResearchClient):
    """Research client using the OpenAI API."""

    provider_name = "openai"

    def __init__(self, config: Config) -> None:
        super().__init__(config)
        if config.openai_api_key:
            self._client = AsyncOpenAI(api_key=config.openai_api_key)
        else:
            self._client = None

    def is_available(self) -> bool:
        return self._client is not None

    async def _do_research(self, prompt: str) -> ResearchResult:
        if self._client is None:
            raise ProviderError("openai", "No API key configured")

        start = time.monotonic()
        try:
            response = await self._client.chat.completions.create(
                model="gpt-4o",
                max_tokens=16384,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a thorough research assistant. Provide comprehensive, "
                            "well-cited research with clear structure and evidence-based findings."
                        ),
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
            )
        except Exception as exc:
            raise ProviderError("openai", str(exc)) from exc

        latency = time.monotonic() - start
        content = response.choices[0].message.content or ""
        tokens = (response.usage.prompt_tokens + response.usage.completion_tokens) if response.usage else 0

        return ResearchResult(
            provider="openai",
            content=content,
            citations=[],
            metadata=ResultMetadata(
                model=response.model,
                tokens_used=tokens,
                latency_s=round(latency, 2),
            ),
        )

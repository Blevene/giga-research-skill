"""Claude (Anthropic) research client."""

from __future__ import annotations

import time

from anthropic import AsyncAnthropic

from giga_research.clients.base import BaseResearchClient
from giga_research.config import Config
from giga_research.errors import ProviderError
from giga_research.models import ResearchResult, ResultMetadata


class ClaudeClient(BaseResearchClient):
    """Research client using the Anthropic API."""

    provider_name = "claude"

    def __init__(self, config: Config) -> None:
        super().__init__(config)
        if config.claude_api_key:
            self._client = AsyncAnthropic(api_key=config.claude_api_key)
        else:
            self._client = None

    def is_available(self) -> bool:
        return self._client is not None

    async def _do_research(self, prompt: str) -> ResearchResult:
        if self._client is None:
            raise ProviderError("claude", "No API key configured")

        start = time.monotonic()
        try:
            message = await self._client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=16384,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                system="You are a thorough research assistant. Provide comprehensive, well-cited research with clear structure and evidence-based findings.",
            )
        except Exception as exc:
            raise ProviderError("claude", str(exc)) from exc

        latency = time.monotonic() - start
        content = message.content[0].text if message.content else ""
        tokens = message.usage.input_tokens + message.usage.output_tokens

        return ResearchResult(
            provider="claude",
            content=content,
            citations=[],
            metadata=ResultMetadata(
                model=message.model,
                tokens_used=tokens,
                latency_s=round(latency, 2),
            ),
        )

"""Claude (Anthropic) research client with web search."""

from __future__ import annotations

import time

from anthropic import AsyncAnthropic

from giga_research.clients.base import BaseResearchClient
from giga_research.config import Config
from giga_research.errors import ProviderError
from giga_research.models import ResearchResult, ResultMetadata

_MODEL = "claude-sonnet-4-5-20250929"


class ClaudeClient(BaseResearchClient):
    """Research client using the Anthropic API with web search."""

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
                model=_MODEL,
                max_tokens=16384,
                messages=[{"role": "user", "content": prompt}],
                tools=[{"type": "web_search_20250305", "name": "web_search", "max_uses": 20}],
                system=(
                    "You are a thorough research assistant with web search capabilities. "
                    "Use web search extensively to find current, accurate information. "
                    "Ground every claim in real sources with verifiable URLs. "
                    "Provide comprehensive, well-cited research with clear structure."
                ),
            )
        except Exception as exc:
            raise ProviderError("claude", str(exc)) from exc

        latency = time.monotonic() - start

        # Extract text from content blocks (web search responses include mixed block types)
        text_parts: list[str] = []
        for block in message.content:
            if hasattr(block, "text"):
                text_parts.append(block.text)
        content = "\n\n".join(text_parts)

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

"""Claude (Anthropic) research client with web search."""

from __future__ import annotations

import time

from anthropic import AsyncAnthropic

from giga_research.clients.base import BaseResearchClient
from giga_research.config import Config
from giga_research.errors import ProviderError
from giga_research.models import Citation, ResearchResult, ResultMetadata

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

        # Extract text and citations from content blocks.
        # Web search responses include: ServerToolUseBlock, WebSearchToolResultBlock, TextBlock.
        # Citations come from two sources:
        #   1. TextBlock.citations — inline citations with url/title/cited_text
        #   2. WebSearchToolResultBlock.content — search result items with url/title
        text_parts: list[str] = []
        seen_urls: set[str] = set()
        extracted_citations: list[Citation] = []

        for block in message.content:
            if hasattr(block, "text"):
                text_parts.append(block.text)
                # Extract inline citations from TextBlock
                if hasattr(block, "citations") and block.citations:
                    for cite in block.citations:
                        if hasattr(cite, "url") and cite.url and cite.url not in seen_urls:
                            seen_urls.add(cite.url)
                            extracted_citations.append(
                                Citation(
                                    text=getattr(cite, "cited_text", ""),
                                    url=cite.url,
                                    title=getattr(cite, "title", None),
                                )
                            )
            elif hasattr(block, "type") and block.type == "web_search_tool_result":
                # Extract URLs from search result blocks
                if hasattr(block, "content") and isinstance(block.content, list):
                    for result in block.content:
                        url = getattr(result, "url", None)
                        if url and url not in seen_urls:
                            seen_urls.add(url)
                            extracted_citations.append(
                                Citation(
                                    text=getattr(result, "title", ""),
                                    url=url,
                                    title=getattr(result, "title", None),
                                )
                            )

        content = "\n\n".join(text_parts)

        tokens = message.usage.input_tokens + message.usage.output_tokens

        return ResearchResult(
            provider="claude",
            content=content,
            citations=extracted_citations,
            metadata=ResultMetadata(
                model=message.model,
                tokens_used=tokens,
                latency_s=round(latency, 2),
            ),
        )

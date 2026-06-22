"""Claude (Anthropic) research client — bounded single-pass web search."""

from __future__ import annotations

import time

from anthropic import AsyncAnthropic

from giga_research.clients.base import BaseResearchClient
from giga_research.config import DEFAULT_CLAUDE_MODEL, Config
from giga_research.errors import ProviderError
from giga_research.models import Citation, ResearchResult, ResultMetadata

# Re-exported for tests / back-compat; the live value comes from config.
_DEFAULT_MODEL = DEFAULT_CLAUDE_MODEL
_BETA = "code-execution-web-tools-2026-02-09"
_MAX_TOKENS = 16000

# Claude is the FAST, BOUNDED provider (OpenAI/Gemini carry exhaustive depth).
# Deliberately web_search ONLY — no web_fetch. Measurement showed web_fetch
# pulls full page bodies, which hits the server-tool iteration cap (returning
# pause_turn with only a preamble), explodes input tokens to millions, and runs
# many minutes. A single web_search pass ends cleanly (~4 min, ~17k-char report).
_TOOLS = [{"type": "web_search_20260209", "name": "web_search", "max_uses": 6}]

_SYSTEM = (
    "You are a focused research assistant with a web search tool. Search "
    "efficiently for current, authoritative information, then write a "
    "well-structured, well-cited report. Prefer depth on the most important "
    "points over exhaustively covering everything. Ground every claim in a real "
    "source with a verifiable URL."
)


class ClaudeClient(BaseResearchClient):
    """Bounded research client using the Anthropic API with web search."""

    provider_name = "claude"
    default_timeout = 600  # bounded provider — fail fast rather than drag for many minutes

    def __init__(self, config: Config) -> None:
        super().__init__(config)
        self._model = config.claude_model
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
        messages: list[dict] = [{"role": "user", "content": prompt}]
        text_parts: list[str] = []
        citations: list[Citation] = []
        seen_urls: set[str] = set()
        tokens = 0
        model = self._model

        try:
            # Single bounded web_search pass — ends with end_turn and a full report.
            message = await self._stream_message(messages, tools=_TOOLS)
            model = message.model
            tokens += message.usage.input_tokens + message.usage.output_tokens
            _extract_blocks(message.content, text_parts, citations, seen_urls)
            messages.append({"role": "assistant", "content": message.content})
            content = "\n\n".join(text_parts).strip()

            # Safety net: if it ever pauses for more tools or returns no prose,
            # force one tools-off pass so a final report is actually written.
            if message.stop_reason == "pause_turn" or not content:
                messages.append(
                    {
                        "role": "user",
                        "content": (
                            "Stop searching now. Using only the sources you have already "
                            "gathered, write the final comprehensive, well-cited research "
                            "report with clear structure."
                        ),
                    }
                )
                final = await self._stream_message(messages, tools=_TOOLS, tool_choice={"type": "none"})
                model = final.model
                tokens += final.usage.input_tokens + final.usage.output_tokens
                _extract_blocks(final.content, text_parts, citations, seen_urls)
                content = "\n\n".join(text_parts).strip()
        except ProviderError:
            raise
        except Exception as exc:
            raise ProviderError("claude", str(exc)) from exc

        latency = time.monotonic() - start
        if not content:
            raise ProviderError(
                "claude",
                f"No synthesis text returned (citations={len(citations)}, tokens={tokens})",
            )

        return ResearchResult(
            provider="claude",
            content=content,
            citations=citations,
            metadata=ResultMetadata(model=model, tokens_used=tokens, latency_s=round(latency, 2)),
        )

    async def _stream_message(self, messages: list[dict], *, tools: list, tool_choice: dict | None = None):
        """One streamed Messages call; returns the final accumulated message."""
        kwargs = {
            "model": self._model,
            "max_tokens": _MAX_TOKENS,
            "betas": [_BETA],
            "messages": messages,
            "tools": tools,
            "system": _SYSTEM,
        }
        if tool_choice is not None:
            kwargs["tool_choice"] = tool_choice
        async with self._client.beta.messages.stream(**kwargs) as stream:
            return await stream.get_final_message()


def _extract_blocks(
    blocks: list,
    text_parts: list[str],
    citations: list[Citation],
    seen_urls: set[str],
) -> None:
    """Accumulate text and citations from one message's content blocks.

    Citations come from inline TextBlock.citations and web_search_tool_result
    blocks, deduplicated by URL.
    """
    for block in blocks:
        if hasattr(block, "text"):
            if block.text:
                text_parts.append(block.text)
            for cite in getattr(block, "citations", None) or []:
                url = getattr(cite, "url", None)
                if url and url not in seen_urls:
                    seen_urls.add(url)
                    citations.append(
                        Citation(
                            text=getattr(cite, "cited_text", "") or "",
                            url=url,
                            title=getattr(cite, "title", None),
                        )
                    )
        elif getattr(block, "type", None) == "web_search_tool_result":
            if isinstance(getattr(block, "content", None), list):
                for result in block.content:
                    url = getattr(result, "url", None)
                    if url and url not in seen_urls:
                        seen_urls.add(url)
                        citations.append(
                            Citation(
                                text=getattr(result, "title", "") or "",
                                url=url,
                                title=getattr(result, "title", None),
                            )
                        )

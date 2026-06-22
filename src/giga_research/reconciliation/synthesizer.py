"""Unified-report synthesis via a single plain LLM call.

This is the one genuinely LLM-dependent pipeline step. Keeping it inside the
pipeline (rather than in a long-lived coordinator subagent) means `orchestrate`
always emits report.md and the skill no longer needs a fragile 25-minute agent.
"""

from __future__ import annotations

from anthropic import AsyncAnthropic

from giga_research.config import Config
from giga_research.models import Citation, ResearchResult

_MAX_TOKENS = 16000

_SYSTEM = (
    "You are a research synthesis editor. You are given several independent research "
    "reports on the same topic from different AI providers, a topic-coverage matrix, and "
    "a validated citation list. Produce ONE unified Markdown report.\n\n"
    "Tag every substantive claim by cross-provider agreement:\n"
    "- **Consensus** — all providers agree (high confidence)\n"
    "- **Majority** — most agree (note the dissent)\n"
    "- **Contested** — providers disagree (present all sides)\n"
    "- **Unique** — only one provider covers it (note single-source)\n\n"
    "Be honest about provenance: if only one provider produced usable prose, say so and do "
    "NOT invent cross-provider agreement. Ground claims in the provided reports; do not add "
    "facts that aren't supported by them. In the References section, prefer citations marked "
    "alive/verified and note ones marked blocked; omit dead ones."
)

_STRUCTURE = (
    "# {topic} — Research Report\n\n"
    "## Executive Summary\n## Methodology\n## Findings\n"
    "(organize Findings by sub-topic; tag each claim consensus/majority/contested/unique and "
    "attribute providers, e.g. [claude, gemini])\n"
    "## Areas of Disagreement\n## Gaps & Limitations\n## References"
)


def _citation_summary(citations: list[Citation], limit: int = 80) -> str:
    """Compact, status-annotated citation list for the synthesis prompt."""
    lines = []
    for c in citations[:limit]:
        if not c.url:
            continue
        status = c.validation_status.value if c.validation_status else "unchecked"
        title = (c.title or "").strip()
        lines.append(f"- [{status}] {c.url}" + (f" — {title}" if title else ""))
    extra = len(citations) - limit
    if extra > 0:
        lines.append(f"- … and {extra} more")
    return "\n".join(lines) if lines else "(none)"


def _build_user_content(
    topic: str,
    results: dict[str, ResearchResult],
    matrix_md: str,
    citations: list[Citation],
) -> str:
    parts = [
        f"# Topic\n{topic}\n",
        "Write the unified report with this structure:\n" + _STRUCTURE,
        "\n# Provider reports\n",
    ]
    for provider, result in results.items():
        parts.append(f"\n## Report from `{provider}` ({result.metadata.model})\n\n{result.content}\n")
    parts.append("\n# Topic-coverage matrix\n\n" + matrix_md)
    parts.append("\n# Validated citations\n\n" + _citation_summary(citations))
    return "\n".join(parts)


async def synthesize_report(
    config: Config,
    topic: str,
    results: dict[str, ResearchResult],
    matrix_md: str,
    citations: list[Citation],
) -> str | None:
    """Synthesize report.md markdown from provider reports, or None if unavailable.

    Uses a single plain (no-tools) Claude call. Returns None when there is no
    Claude API key or nothing to synthesize, so the pipeline degrades gracefully.
    """
    if not config.claude_api_key or not results:
        return None

    client = AsyncAnthropic(api_key=config.claude_api_key)
    user_content = _build_user_content(topic, results, matrix_md, citations)
    message = await client.messages.create(
        model=config.claude_model,
        max_tokens=_MAX_TOKENS,
        system=_SYSTEM,
        messages=[{"role": "user", "content": user_content}],
    )
    text = "".join(getattr(block, "text", "") or "" for block in message.content)
    return text.strip() or None

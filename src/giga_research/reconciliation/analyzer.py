"""Cross-report analysis: citation extraction, dedup, and comparison."""

from __future__ import annotations

import re

from giga_research.models import Citation, ResearchResult


def extract_citations_from_markdown(content: str) -> list[Citation]:
    """Extract citations from markdown content (links and bare URLs)."""
    citations: list[Citation] = []
    seen_urls: set[str] = set()

    # Markdown links: [title](url)
    for match in re.finditer(r"\[([^\]]+)\]\((https?://[^\s)]+)\)", content):
        title, url = match.group(1), match.group(2)
        if url not in seen_urls:
            start = max(0, match.start() - 100)
            end = min(len(content), match.end() + 100)
            context = content[start:end].strip()
            citations.append(Citation(text=context, url=url, title=title))
            seen_urls.add(url)

    # Bare URLs not already captured
    for match in re.finditer(r"(?<!\()(https?://[^\s)\]>,]+)", content):
        url = match.group(1).rstrip(".")
        if url not in seen_urls:
            start = max(0, match.start() - 100)
            end = min(len(content), match.end() + 100)
            context = content[start:end].strip()
            citations.append(Citation(text=context, url=url))
            seen_urls.add(url)

    return citations


def deduplicate_citations(citations: list[Citation]) -> list[Citation]:
    """Deduplicate citations by URL, keeping the first occurrence."""
    seen: dict[str, Citation] = {}
    for c in citations:
        key = c.url or c.text
        if key not in seen:
            seen[key] = c
    return list(seen.values())


def _extract_sections(content: str) -> dict[str, str]:
    """Extract h2 sections from markdown content."""
    sections: dict[str, str] = {}
    current_heading: str | None = None
    current_lines: list[str] = []

    for line in content.split("\n"):
        h2_match = re.match(r"^##\s+(.+)$", line)
        if h2_match:
            if current_heading is not None:
                sections[current_heading] = "\n".join(current_lines).strip()
            current_heading = h2_match.group(1).strip()
            current_lines = []
        elif current_heading is not None:
            current_lines.append(line)

    if current_heading is not None:
        sections[current_heading] = "\n".join(current_lines).strip()

    return sections


def build_comparison_matrix(
    results: dict[str, ResearchResult],
) -> dict[str, dict[str, str | None]]:
    """Build a topic-by-provider comparison matrix.

    Returns:
        Dict mapping topic name -> {provider: content_summary | None}
    """
    provider_sections: dict[str, dict[str, str]] = {}
    for provider, result in results.items():
        provider_sections[provider] = _extract_sections(result.content)

    all_topics: set[str] = set()
    for sections in provider_sections.values():
        all_topics.update(sections.keys())

    matrix: dict[str, dict[str, str | None]] = {}
    for topic in sorted(all_topics):
        matrix[topic] = {}
        for provider in results:
            content = provider_sections[provider].get(topic)
            matrix[topic][provider] = content

    return matrix

"""Build structured markdown output files from analysis results."""

from __future__ import annotations

from giga_research.models import Citation


def build_comparison_markdown(matrix: dict[str, dict[str, str | None]]) -> str:
    """Build a comparison matrix markdown document."""
    if not matrix:
        return "# Comparison Matrix\n\nNo topics to compare.\n"

    providers = set()
    for topic_data in matrix.values():
        providers.update(topic_data.keys())
    providers_list = sorted(providers)

    lines = ["# Comparison Matrix\n"]
    lines.append("| Topic | " + " | ".join(providers_list) + " |")
    lines.append("|" + "---|" * (len(providers_list) + 1))

    for topic, provider_data in matrix.items():
        cells = []
        for p in providers_list:
            content = provider_data.get(p)
            if content:
                summary = content.split(".")[0].strip()
                if len(summary) > 80:
                    summary = summary[:77] + "..."
                cells.append(summary)
            else:
                cells.append("*not covered*")
        lines.append(f"| {topic} | " + " | ".join(cells) + " |")

    lines.append("")
    lines.append("## Detailed Comparison\n")
    for topic, provider_data in matrix.items():
        lines.append(f"### {topic}\n")
        for p in providers_list:
            content = provider_data.get(p)
            if content:
                lines.append(f"**{p}:** {content}\n")
            else:
                lines.append(f"**{p}:** *Not covered by this provider.*\n")
        lines.append("")

    return "\n".join(lines)


def build_validation_log(citations: list[Citation]) -> str:
    """Build a citation validation log markdown document."""
    if not citations:
        return "# Citation Validation Log\n\nNo citations to validate.\n"

    lines = ["# Citation Validation Log\n"]

    status_counts: dict[str, int] = {}
    for c in citations:
        status = c.validation_status.value
        status_counts[status] = status_counts.get(status, 0) + 1

    lines.append("## Summary\n")
    for status, count in sorted(status_counts.items()):
        lines.append(f"- **{status}**: {count}")
    lines.append("")

    lines.append("## Details\n")
    lines.append("| Status | URL | Claim (excerpt) |")
    lines.append("|---|---|---|")

    for c in citations:
        url = c.url or "*no URL*"
        claim = c.text[:80].replace("|", "\\|")
        if len(c.text) > 80:
            claim += "..."
        status = c.validation_status.value.upper()
        lines.append(f"| {status} | {url} | {claim} |")

    lines.append("")
    return "\n".join(lines)

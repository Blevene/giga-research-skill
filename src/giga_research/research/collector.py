"""Result collection, file I/O, and session management."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

from giga_research.models import ResearchResult


def _slugify(text: str) -> str:
    """Convert text to a URL-safe slug."""
    slug = text.lower().strip()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug)
    return slug[:50].strip("-")


def create_session_dir(output_dir: Path, topic: str) -> Path:
    """Create a timestamped session directory with raw/ subdirectory."""
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    slug = _slugify(topic)
    session_dir = output_dir / f"{timestamp}-{slug}"
    session_dir.mkdir(parents=True, exist_ok=True)
    (session_dir / "raw").mkdir(exist_ok=True)
    return session_dir


def save_result_to_file(session_dir: Path, result: ResearchResult) -> Path:
    """Save a research result's content to raw/<provider>.md."""
    raw_file = session_dir / "raw" / f"{result.provider}.md"
    raw_file.write_text(result.content, encoding="utf-8")

    # Also save the full result as JSON for metadata preservation
    json_file = session_dir / "raw" / f"{result.provider}.json"
    json_file.write_text(result.model_dump_json(indent=2), encoding="utf-8")

    return raw_file


def load_result_from_file(session_dir: Path, provider: str) -> ResearchResult | None:
    """Load a research result from the session directory."""
    json_file = session_dir / "raw" / f"{provider}.json"
    if not json_file.exists():
        return None
    return ResearchResult.model_validate_json(json_file.read_text(encoding="utf-8"))


def save_session_metadata(
    session_dir: Path,
    *,
    providers_used: list[str],
    providers_skipped: list[str],
    citation_validation_depth: int,
    results: dict[str, ResearchResult],
) -> Path:
    """Save session metadata as meta.json."""
    meta = {
        "session_id": session_dir.name,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "providers_used": providers_used,
        "providers_skipped": providers_skipped,
        "citation_validation_depth": citation_validation_depth,
        "provider_metadata": {
            name: {
                "model": r.metadata.model,
                "tokens_used": r.metadata.tokens_used,
                "latency_s": r.metadata.latency_s,
            }
            for name, r in results.items()
        },
    }
    meta_file = session_dir / "meta.json"
    meta_file.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    return meta_file

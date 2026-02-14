"""Tests for result collection and file I/O."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from giga_research.models import ResearchResult, ResultMetadata
from giga_research.research.collector import (
    create_session_dir,
    load_result_from_file,
    save_result_to_file,
    save_session_metadata,
)


@pytest.fixture
def tmp_output(tmp_path: Path) -> Path:
    return tmp_path / "research-output"


def _make_result(provider: str) -> ResearchResult:
    return ResearchResult(
        provider=provider,
        content=f"# Report from {provider}\n\nFindings here.",
        citations=[],
        metadata=ResultMetadata(model=f"{provider}-model", tokens_used=100, latency_s=1.0),
    )


def test_create_session_dir(tmp_output: Path):
    session_dir = create_session_dir(tmp_output, "quantum computing")
    assert session_dir.exists()
    assert "quantum-computing" in session_dir.name
    assert (session_dir / "raw").is_dir()


def test_save_result_to_file(tmp_output: Path):
    session_dir = create_session_dir(tmp_output, "test topic")
    result = _make_result("claude")
    save_result_to_file(session_dir, result)
    raw_file = session_dir / "raw" / "claude.md"
    assert raw_file.exists()
    assert "Report from claude" in raw_file.read_text()


def test_load_result_from_file(tmp_output: Path):
    session_dir = create_session_dir(tmp_output, "test topic")
    result = _make_result("openai")
    save_result_to_file(session_dir, result)
    loaded = load_result_from_file(session_dir, "openai")
    assert loaded is not None
    assert loaded.provider == "openai"


def test_load_result_missing_file(tmp_output: Path):
    session_dir = create_session_dir(tmp_output, "test topic")
    loaded = load_result_from_file(session_dir, "gemini")
    assert loaded is None


def test_save_session_metadata(tmp_output: Path):
    session_dir = create_session_dir(tmp_output, "test topic")
    results = {"claude": _make_result("claude")}
    save_session_metadata(
        session_dir,
        providers_used=["claude"],
        providers_skipped=["openai", "gemini"],
        citation_validation_depth=1,
        results=results,
    )
    meta_file = session_dir / "meta.json"
    assert meta_file.exists()
    meta = json.loads(meta_file.read_text())
    assert meta["providers_used"] == ["claude"]
    assert meta["providers_skipped"] == ["openai", "gemini"]
    assert "claude" in meta["provider_metadata"]

"""Tests for output file writer."""

from __future__ import annotations

from pathlib import Path

import pytest

from giga_research.models import Citation, ValidationStatus
from giga_research.output.writer import write_all_outputs


@pytest.fixture
def session_dir(tmp_path: Path) -> Path:
    d = tmp_path / "session"
    d.mkdir()
    (d / "raw").mkdir()
    return d


def test_write_all_outputs_creates_files(session_dir: Path):
    citations = [
        Citation(text="A claim", url="https://a.com", validation_status=ValidationStatus.VERIFIED),
    ]
    matrix = {"Findings": {"claude": "claude found things.", "openai": "openai found things."}}

    write_all_outputs(
        session_dir=session_dir,
        unified_report="# Unified Report\n\nSynthesized content.",
        comparison_matrix=matrix,
        validated_citations=citations,
        prompt="Research quantum computing",
    )

    assert (session_dir / "report.md").exists()
    assert (session_dir / "comparison-matrix.md").exists()
    assert (session_dir / "validation-log.md").exists()
    assert (session_dir / "prompt.md").exists()


def test_write_all_outputs_content(session_dir: Path):
    write_all_outputs(
        session_dir=session_dir,
        unified_report="# Report\n\nContent here.",
        comparison_matrix={},
        validated_citations=[],
        prompt="Test prompt",
    )

    report = (session_dir / "report.md").read_text()
    assert "Content here" in report

    prompt = (session_dir / "prompt.md").read_text()
    assert "Test prompt" in prompt

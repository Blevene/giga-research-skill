"""Tests for the orchestrate CLI subcommand."""

from __future__ import annotations

import json
import subprocess
import sys
from unittest.mock import AsyncMock, patch

import pytest

from giga_research.cli import main
from giga_research.orchestration.pipeline import PipelineResult


def test_orchestrate_json_output(session_dir, capsys):
    """orchestrate outputs valid JSON with expected fields."""
    fake_result = PipelineResult(
        session_dir=str(session_dir),
        providers_used=["claude"],
        providers_failed={},
        citation_count=2,
        citations_validated=0,
        topics_identified=["Intro"],
    )

    with patch("giga_research.orchestration.pipeline.run_pipeline", new_callable=AsyncMock, return_value=fake_result):
        main(["orchestrate", "--session-dir", str(session_dir)])

    captured = capsys.readouterr()
    output = json.loads(captured.out)
    assert output["providers_used"] == ["claude"]
    assert output["session_dir"] == str(session_dir)
    assert "citation_count" in output
    assert "topics_identified" in output


def test_orchestrate_missing_session_dir(tmp_path):
    """Missing session dir exits with error."""
    nonexistent = str(tmp_path / "does-not-exist")
    with pytest.raises(SystemExit) as exc_info:
        main(["orchestrate", "--session-dir", nonexistent])
    assert exc_info.value.code == 1


def test_orchestrate_missing_prompt(tmp_path):
    """Session dir without prompt.md exits with error."""
    sdir = tmp_path / "no-prompt"
    sdir.mkdir()
    with pytest.raises(SystemExit) as exc_info:
        main(["orchestrate", "--session-dir", str(sdir)])
    assert exc_info.value.code == 1


def test_orchestrate_help():
    """orchestrate --help shows usage."""
    result = subprocess.run(
        [sys.executable, "-m", "giga_research.cli", "orchestrate", "--help"],
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert result.returncode == 0
    assert "--session-dir" in result.stdout
    assert "--depth" in result.stdout

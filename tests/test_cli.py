"""Tests for CLI interface."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from giga_research.cli import _load_client_class, main


def test_load_client_class_success():
    """_load_client_class returns the correct class for an installed provider."""
    cls = _load_client_class("claude")
    assert cls.__name__ == "ClaudeClient"


def test_load_client_class_missing_sdk():
    """_load_client_class raises ImportError with install hint when SDK is missing."""
    with (
        patch("importlib.import_module", side_effect=ImportError("no module")),
        pytest.raises(ImportError, match='pip install "giga-research\\[claude\\]"'),
    ):
        _load_client_class("claude")


def test_check_providers_no_keys(capsys, monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    main(["check-providers"])
    captured = capsys.readouterr()
    assert "available" in captured.out.lower() or "Available" in captured.out


def test_check_providers_with_keys(capsys, monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test")
    monkeypatch.setenv("OPENAI_API_KEY", "test")
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    main(["check-providers"])
    captured = capsys.readouterr()
    assert "claude" in captured.out.lower()
    assert "openai" in captured.out.lower()


def test_create_session_prints_path(capsys, tmp_path):
    """create-session creates a directory and prints its absolute path."""
    main(["create-session", "--topic", "test-topic", "--output-dir", str(tmp_path)])
    captured = capsys.readouterr()
    session_path = Path(captured.out.strip())
    assert session_path.is_absolute()
    assert session_path.exists()
    assert (session_path / "raw").exists()
    assert "test-topic" in session_path.name


def test_create_session_custom_output_dir(capsys, tmp_path):
    """create-session respects --output-dir."""
    custom_dir = tmp_path / "custom-output"
    main(["create-session", "--topic", "my-research", "--output-dir", str(custom_dir)])
    captured = capsys.readouterr()
    session_path = Path(captured.out.strip())
    assert str(custom_dir) in str(session_path)
    assert session_path.exists()


def test_cli_module_runnable():
    """Verify the module can be invoked via python -m."""
    result = subprocess.run(
        [sys.executable, "-m", "giga_research.cli", "check-providers"],
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert result.returncode == 0


def test_uv_run_project_check_providers(tmp_path):
    """Verify check-providers works via uv run --project from a different CWD."""
    from giga_research.config import SKILL_ROOT

    result = subprocess.run(
        ["uv", "run", "--project", str(SKILL_ROOT), "giga-research", "check-providers"],
        capture_output=True,
        text=True,
        timeout=30,
        cwd=str(tmp_path),
    )
    assert result.returncode == 0
    assert "available" in result.stdout.lower()


def test_uv_run_project_create_session(tmp_path):
    """Verify create-session works via uv run --project from a different CWD."""
    from giga_research.config import SKILL_ROOT

    result = subprocess.run(
        [
            "uv", "run", "--project", str(SKILL_ROOT),
            "giga-research", "create-session",
            "--topic", "integration-test",
            "--output-dir", str(tmp_path),
        ],
        capture_output=True,
        text=True,
        timeout=30,
        cwd=str(tmp_path),
    )
    assert result.returncode == 0
    session_path = Path(result.stdout.strip())
    assert session_path.is_absolute()
    assert session_path.exists()
    assert "integration-test" in session_path.name

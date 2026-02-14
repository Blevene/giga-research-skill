"""Tests for CLI interface."""

from __future__ import annotations

import subprocess
import sys

import pytest

from giga_research.cli import main


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


def test_cli_module_runnable():
    """Verify the module can be invoked via python -m."""
    result = subprocess.run(
        [sys.executable, "-m", "giga_research.cli", "check-providers"],
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert result.returncode == 0

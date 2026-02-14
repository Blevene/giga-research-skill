"""Shared test fixtures for giga_research."""

from __future__ import annotations

import pytest

from giga_research.config import Config


@pytest.fixture
def config_no_keys() -> Config:
    """Config with no API keys set."""
    return Config()


@pytest.fixture
def config_all_keys() -> Config:
    """Config with all API keys set."""
    return Config(
        claude_api_key="test-claude-key",
        openai_api_key="test-openai-key",
        gemini_api_key="test-gemini-key",
    )


@pytest.fixture
def session_dir(tmp_path):
    """Create a session directory with prompt.md and raw/ subdirectory."""
    sdir = tmp_path / "test-session"
    sdir.mkdir()
    (sdir / "raw").mkdir()
    (sdir / "prompt.md").write_text("# Research Task: Test Topic\n\nResearch this.", encoding="utf-8")
    return sdir

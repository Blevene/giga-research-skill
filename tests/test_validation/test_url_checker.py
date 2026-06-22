"""Tests for URL probing and the reachable/blocked/dead taxonomy."""

from __future__ import annotations

import httpx
import respx

from giga_research.models import ValidationStatus
from giga_research.validation.url_checker import probe_url


@respx.mock
async def test_probe_alive_with_body():
    respx.get("https://example.com/page").mock(
        return_value=httpx.Response(200, text="<html><body>The claim is here.</body></html>")
    )
    status, body = await probe_url("https://example.com/page", fetch_body=True)
    assert status == ValidationStatus.ALIVE
    assert body is not None
    assert "claim is here" in body


@respx.mock
async def test_probe_alive_no_body_when_not_requested():
    respx.get("https://example.com/page").mock(return_value=httpx.Response(200, text="<html>hi</html>"))
    status, body = await probe_url("https://example.com/page")
    assert status == ValidationStatus.ALIVE
    assert body is None


@respx.mock
async def test_probe_404_is_dead():
    respx.get("https://example.com/gone").mock(return_value=httpx.Response(404))
    status, _ = await probe_url("https://example.com/gone")
    assert status == ValidationStatus.DEAD


@respx.mock
async def test_probe_403_is_blocked_not_dead():
    """A forbidden/anti-bot response means the page exists — BLOCKED, not DEAD."""
    respx.get("https://example.com/protected").mock(return_value=httpx.Response(403))
    status, _ = await probe_url("https://example.com/protected")
    assert status == ValidationStatus.BLOCKED


@respx.mock
async def test_probe_500_is_blocked():
    respx.get("https://example.com/err").mock(return_value=httpx.Response(500))
    status, _ = await probe_url("https://example.com/err")
    assert status == ValidationStatus.BLOCKED


@respx.mock
async def test_probe_timeout_is_blocked():
    respx.get("https://example.com/slow").mock(side_effect=httpx.TimeoutException("timeout"))
    status, _ = await probe_url("https://example.com/slow")
    assert status == ValidationStatus.BLOCKED


@respx.mock
async def test_probe_connect_error_is_dead():
    respx.get("https://nope.invalid/x").mock(side_effect=httpx.ConnectError("dns fail"))
    status, _ = await probe_url("https://nope.invalid/x")
    assert status == ValidationStatus.DEAD

"""Tests for URL liveness and content checking."""

from __future__ import annotations

import httpx
import pytest
import respx

from giga_research.validation.url_checker import check_url_alive, fetch_url_content


@respx.mock
async def test_check_url_alive_success():
    respx.head("https://example.com/article").mock(return_value=httpx.Response(200))
    result = await check_url_alive("https://example.com/article")
    assert result is True


@respx.mock
async def test_check_url_alive_404():
    respx.head("https://example.com/gone").mock(return_value=httpx.Response(404))
    result = await check_url_alive("https://example.com/gone")
    assert result is False


@respx.mock
async def test_check_url_alive_timeout():
    respx.head("https://example.com/slow").mock(side_effect=httpx.TimeoutException("timeout"))
    result = await check_url_alive("https://example.com/slow")
    assert result is False


@respx.mock
async def test_fetch_url_content_success():
    respx.get("https://example.com/page").mock(
        return_value=httpx.Response(200, text="<html><body>The claim is here.</body></html>")
    )
    content = await fetch_url_content("https://example.com/page")
    assert content is not None
    assert "claim is here" in content


@respx.mock
async def test_fetch_url_content_failure():
    respx.get("https://example.com/fail").mock(return_value=httpx.Response(500))
    content = await fetch_url_content("https://example.com/fail")
    assert content is None


@respx.mock
async def test_fetch_url_content_timeout():
    respx.get("https://example.com/slow").mock(side_effect=httpx.TimeoutException("timeout"))
    content = await fetch_url_content("https://example.com/slow")
    assert content is None

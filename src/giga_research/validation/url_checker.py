"""URL liveness and content fetching."""

from __future__ import annotations

import re

import httpx

_TIMEOUT = httpx.Timeout(15.0, connect=5.0)
_HEADERS = {"User-Agent": "giga-research-validator/0.1"}


async def check_url_alive(url: str) -> bool:
    """Check if a URL resolves with HTTP 2xx."""
    try:
        async with httpx.AsyncClient(timeout=_TIMEOUT, headers=_HEADERS, follow_redirects=True) as client:
            resp = await client.head(url)
            return resp.is_success
    except (httpx.HTTPError, httpx.InvalidURL):
        return False


async def fetch_url_content(url: str) -> str | None:
    """Fetch a URL and return text content, stripped of HTML tags. None on failure."""
    try:
        async with httpx.AsyncClient(timeout=_TIMEOUT, headers=_HEADERS, follow_redirects=True) as client:
            resp = await client.get(url)
            if not resp.is_success:
                return None
            text = resp.text
            # Strip HTML tags for simple text comparison
            text = re.sub(r"<[^>]+>", " ", text)
            text = re.sub(r"\s+", " ", text).strip()
            return text
    except (httpx.HTTPError, httpx.InvalidURL):
        return None

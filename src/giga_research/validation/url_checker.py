"""URL liveness probing with an honest reachable/blocked/dead taxonomy."""

from __future__ import annotations

import re

import httpx

from giga_research.models import ValidationStatus

_TIMEOUT = httpx.Timeout(15.0, connect=5.0)
# A realistic browser UA — many authoritative sources (CISA, Cloudflare-fronted
# sites) return 403 to obvious bot agents, which previously got mislabeled DEAD.
_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

# Status codes that mean "the page is genuinely gone."
_DEAD_CODES = {404, 410}


def _strip_html(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


async def probe_url(url: str, *, fetch_body: bool = False) -> tuple[ValidationStatus, str | None]:
    """Probe a URL, returning (status, body).

    - ALIVE  — 2xx. ``body`` is stripped page text when ``fetch_body`` is set.
    - DEAD   — 404/410, unresolvable host, or invalid URL (likely fabricated/gone).
    - BLOCKED — anything else non-2xx (401/403/405/429/5xx), timeout, or transport
                error: the page very likely exists, we just couldn't read it.

    A GET (not HEAD) with a browser User-Agent is used because many servers
    reject HEAD or bot agents with 403/405, which must NOT be read as "dead".
    """
    try:
        async with httpx.AsyncClient(timeout=_TIMEOUT, headers=_HEADERS, follow_redirects=True) as client:
            resp = await client.get(url)
    except httpx.InvalidURL:
        return ValidationStatus.DEAD, None
    except httpx.ConnectError:
        # Host doesn't resolve / refuses the connection — treat as dead.
        return ValidationStatus.DEAD, None
    except httpx.HTTPError:
        # Timeouts and other transport errors — exists-but-unreachable.
        return ValidationStatus.BLOCKED, None

    if resp.is_success:
        return ValidationStatus.ALIVE, (_strip_html(resp.text) if fetch_body else None)
    if resp.status_code in _DEAD_CODES:
        return ValidationStatus.DEAD, None
    return ValidationStatus.BLOCKED, None

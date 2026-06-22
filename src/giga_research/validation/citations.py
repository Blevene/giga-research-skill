"""Citation validation at configurable depth levels."""

from __future__ import annotations

import asyncio

from giga_research.models import Citation, ValidationStatus
from giga_research.validation.url_checker import probe_url


def _text_contains_claim(page_text: str, claim: str) -> bool:
    """Heuristic: do the claim's significant words (>4 chars) appear on the page?

    A weak positive signal only — used to mark VERIFIED vs UNVERIFIED, never to
    accuse a citation of being fabricated (a missing match can mean paraphrase,
    JS-rendered content, or a snippet/title that isn't verbatim in the body).
    """
    words = [w.lower() for w in claim.split() if len(w) > 4]
    if not words:
        return bool(claim.strip()) and claim.lower() in page_text.lower()
    page_lower = page_text.lower()
    matches = sum(1 for w in words if w in page_lower)
    return matches >= len(words) * 0.6


async def _validate_one(
    citation: Citation,
    depth: int,
    semaphore: asyncio.Semaphore,
) -> Citation:
    """Validate a single citation at the given depth.

    Depth 1: liveness — ALIVE / BLOCKED / DEAD.
    Depth 2+: also fetch the body; on a live page, VERIFIED if the claim's words
    appear, else UNVERIFIED. BLOCKED/DEAD are preserved (never downgraded to a
    verification verdict — we can't judge a page we couldn't read).
    """
    if not citation.url or depth == 0:
        return citation

    async with semaphore:
        status, body = await probe_url(citation.url, fetch_body=depth >= 2)
        if depth >= 2 and status == ValidationStatus.ALIVE and body is not None:
            status = (
                ValidationStatus.VERIFIED
                if _text_contains_claim(body, citation.text)
                else ValidationStatus.UNVERIFIED
            )
        return citation.model_copy(update={"validation_status": status})


async def validate_citations(
    citations: list[Citation],
    depth: int = 0,
    max_concurrent: int = 10,
) -> list[Citation]:
    """Validate a list of citations at the specified depth.

    Depth levels:
        0: No validation (return as-is)
        1: URL liveness check (HEAD request)
        2: Content verification (fetch + claim matching)
        3: Full verification + replacement search (TODO: web search fallback)
    """
    if depth == 0:
        return citations

    semaphore = asyncio.Semaphore(max_concurrent)
    tasks = [_validate_one(c, depth, semaphore) for c in citations]
    return list(await asyncio.gather(*tasks))

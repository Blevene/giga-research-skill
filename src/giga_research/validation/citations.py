"""Citation validation at configurable depth levels."""

from __future__ import annotations

import asyncio

from giga_research.models import Citation, ValidationStatus
from giga_research.validation.url_checker import check_url_alive, fetch_url_content


def _text_contains_claim(page_text: str, claim: str) -> bool:
    """Check if a page's text contains the essence of a claim.

    Uses significant words from the claim (>4 chars) to check presence.
    """
    words = [w.lower() for w in claim.split() if len(w) > 4]
    if not words:
        return claim.lower() in page_text.lower()
    page_lower = page_text.lower()
    matches = sum(1 for w in words if w in page_lower)
    return matches >= len(words) * 0.6


async def _validate_one(
    citation: Citation,
    depth: int,
    semaphore: asyncio.Semaphore,
) -> Citation:
    """Validate a single citation at the given depth."""
    if not citation.url or depth == 0:
        return citation

    async with semaphore:
        if depth == 1:
            alive = await check_url_alive(citation.url)
            return citation.model_copy(
                update={"validation_status": ValidationStatus.ALIVE if alive else ValidationStatus.DEAD}
            )

        # Depth 2+: fetch content and verify claim
        content = await fetch_url_content(citation.url)
        if content is None:
            return citation.model_copy(update={"validation_status": ValidationStatus.DEAD})

        if _text_contains_claim(content, citation.text):
            return citation.model_copy(update={"validation_status": ValidationStatus.VERIFIED})
        else:
            return citation.model_copy(update={"validation_status": ValidationStatus.HALLUCINATED})


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

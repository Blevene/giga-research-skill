"""Full deterministic research pipeline: dispatch → validate → compare."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel

from giga_research.clients.base import BaseResearchClient
from giga_research.config import ALL_PROVIDERS, Config
from giga_research.models import Citation, ValidationStatus
from giga_research.reconciliation.analyzer import (
    build_comparison_matrix,
    deduplicate_citations,
    extract_citations_from_markdown,
)
from giga_research.reconciliation.report_builder import (
    build_comparison_markdown,
    build_validation_log,
)
from giga_research.research.collector import save_result_to_file, save_session_metadata
from giga_research.research.dispatcher import dispatch_research
from giga_research.validation.citations import validate_citations


class PipelineResult(BaseModel):
    """Summary of a completed pipeline run."""

    session_dir: str
    providers_used: list[str]
    providers_failed: dict[str, str] = {}
    citation_count: int = 0
    citations_validated: int = 0
    topics_identified: list[str] = []


def _build_clients(config: Config) -> list[BaseResearchClient]:
    """Build client instances for all available providers."""
    from giga_research.clients.claude import ClaudeClient
    from giga_research.clients.gemini import GeminiClient
    from giga_research.clients.openai_client import OpenAIClient

    client_classes: list[type[BaseResearchClient]] = [ClaudeClient, OpenAIClient, GeminiClient]
    clients: list[BaseResearchClient] = []
    for cls in client_classes:
        client = cls(config)
        if client.is_available():
            clients.append(client)
    return clients


async def run_pipeline(
    session_dir: Path,
    *,
    depth: int = 0,
    config: Config | None = None,
    clients: list[BaseResearchClient] | None = None,
) -> PipelineResult:
    """Run the full deterministic research pipeline.

    Args:
        session_dir: Path to session directory (must contain prompt.md).
        depth: Citation validation depth (0-3).
        config: Optional config override. Loaded from env if not provided.
        clients: Optional client list override. Built from config if not provided.

    Returns:
        PipelineResult with summary of the run.
    """
    if config is None:
        config = Config.from_env()

    if clients is None:
        clients = _build_clients(config)

    # 0. Ensure raw/ directory exists
    (session_dir / "raw").mkdir(exist_ok=True)

    # 1. Read prompt
    prompt_file = session_dir / "prompt.md"
    if not prompt_file.exists():
        raise FileNotFoundError(f"prompt.md not found in {session_dir}")
    prompt = prompt_file.read_text(encoding="utf-8")

    # 2. Dispatch research to all available providers in parallel
    results, errors = await dispatch_research(prompt, clients)

    # 3. Save each successful result to raw/<provider>.md + .json
    for result in results.values():
        save_result_to_file(session_dir, result)

    # 4. Extract and deduplicate citations from markdown + ResearchResult.citations
    all_citations: list[Citation] = []
    for result in results.values():
        all_citations.extend(extract_citations_from_markdown(result.content))
        all_citations.extend(result.citations)
    all_citations = deduplicate_citations(all_citations)

    # 5. Validate citations at requested depth
    validated = await validate_citations(all_citations, depth=depth)

    # 6. Build comparison matrix
    matrix = build_comparison_matrix(results)

    # 7. Write structural outputs
    matrix_md = build_comparison_markdown(matrix)
    (session_dir / "comparison-matrix.md").write_text(matrix_md, encoding="utf-8")

    val_log = build_validation_log(validated)
    (session_dir / "validation-log.md").write_text(val_log, encoding="utf-8")

    # 8. Save session metadata
    providers_used = list(results.keys())
    providers_skipped = [p for p in ALL_PROVIDERS if p not in providers_used and p not in errors]
    save_session_metadata(
        session_dir,
        providers_used=providers_used,
        providers_skipped=providers_skipped,
        citation_validation_depth=depth,
        results=results,
    )

    return PipelineResult(
        session_dir=str(session_dir),
        providers_used=providers_used,
        providers_failed={name: str(exc) for name, exc in errors.items()},
        citation_count=len(all_citations),
        citations_validated=sum(1 for c in validated if c.validation_status != ValidationStatus.UNCHECKED),
        topics_identified=list(matrix.keys()),
    )

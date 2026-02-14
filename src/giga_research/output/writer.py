"""Write all output artifacts to the session directory."""

from __future__ import annotations

from pathlib import Path

from giga_research.models import Citation
from giga_research.reconciliation.report_builder import (
    build_comparison_markdown,
    build_validation_log,
)


def write_all_outputs(
    *,
    session_dir: Path,
    unified_report: str,
    comparison_matrix: dict[str, dict[str, str | None]],
    validated_citations: list[Citation],
    prompt: str,
) -> None:
    """Write all output files to the session directory."""
    (session_dir / "report.md").write_text(unified_report, encoding="utf-8")

    matrix_md = build_comparison_markdown(comparison_matrix)
    (session_dir / "comparison-matrix.md").write_text(matrix_md, encoding="utf-8")

    val_log = build_validation_log(validated_citations)
    (session_dir / "validation-log.md").write_text(val_log, encoding="utf-8")

    (session_dir / "prompt.md").write_text(prompt, encoding="utf-8")

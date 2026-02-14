"""CLI interface for giga_research, invoked by subagents."""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

from giga_research.config import ALL_PROVIDERS, Config


def _cmd_check_providers(config: Config) -> None:
    """Report which API keys are configured."""
    available = config.available_providers
    missing = [p for p in ALL_PROVIDERS if p not in available]

    print(f"Available providers: {', '.join(available) if available else 'none'}")
    if missing:
        print(f"Missing providers: {', '.join(missing)}")
    print(json.dumps({"available": available, "missing": missing}))


def _cmd_research(args: argparse.Namespace, config: Config) -> None:
    """Run research on a single provider."""
    from giga_research.clients.claude import ClaudeClient
    from giga_research.clients.gemini import GeminiClient
    from giga_research.clients.openai_client import OpenAIClient
    from giga_research.research.collector import save_result_to_file

    prompt_file = Path(args.prompt_file)
    if not prompt_file.exists():
        print(f"Error: prompt file not found: {prompt_file}", file=sys.stderr)
        sys.exit(1)
    prompt = prompt_file.read_text(encoding="utf-8")

    session_dir = Path(args.session_dir)
    if not session_dir.exists():
        print(f"Error: session dir not found: {session_dir}", file=sys.stderr)
        sys.exit(1)

    client_map = {
        "claude": ClaudeClient,
        "openai": OpenAIClient,
        "gemini": GeminiClient,
    }
    provider = args.provider
    if provider not in client_map:
        print(f"Error: unknown provider: {provider}", file=sys.stderr)
        sys.exit(1)

    client = client_map[provider](config)
    if not client.is_available():
        print(f"Error: {provider} API key not configured", file=sys.stderr)
        sys.exit(1)

    result = asyncio.run(client.research(prompt))
    save_result_to_file(session_dir, result)
    print(f"Research complete. Result saved to {session_dir}/raw/{provider}.md")
    output = {
        "provider": provider,
        "tokens_used": result.metadata.tokens_used,
        "latency_s": result.metadata.latency_s,
    }
    print(json.dumps(output))


def _cmd_orchestrate(args: argparse.Namespace, config: Config) -> None:
    """Run the full deterministic pipeline for a session."""
    from giga_research.orchestration.pipeline import run_pipeline

    session_dir = Path(args.session_dir)
    if not session_dir.exists():
        print(json.dumps({"error": f"session dir not found: {session_dir}"}), file=sys.stderr)
        sys.exit(1)
    if not (session_dir / "prompt.md").exists():
        print(json.dumps({"error": f"prompt.md not found in {session_dir}"}), file=sys.stderr)
        sys.exit(1)

    depth = args.depth
    try:
        result = asyncio.run(run_pipeline(session_dir, depth=depth, config=config))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        sys.exit(1)
    print(json.dumps(result.model_dump(), indent=2))


def _cmd_validate(args: argparse.Namespace, config: Config) -> None:
    """Validate citations from collected reports."""
    from giga_research.reconciliation.analyzer import extract_citations_from_markdown
    from giga_research.reconciliation.report_builder import build_validation_log
    from giga_research.validation.citations import validate_citations

    session_dir = Path(args.session_dir)
    raw_dir = session_dir / "raw"

    all_citations = []
    for md_file in raw_dir.glob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        all_citations.extend(extract_citations_from_markdown(content))

    depth = args.depth
    validated = asyncio.run(validate_citations(all_citations, depth=depth))

    log = build_validation_log(validated)
    log_file = session_dir / "validation-log.md"
    log_file.write_text(log, encoding="utf-8")

    print(f"Validated {len(validated)} citations at depth {depth}")
    print(f"Log written to {log_file}")


def main(argv: list[str] | None = None) -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(prog="giga_research", description="Multi-provider deep research")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("check-providers", help="Report which API keys are configured")

    research_p = sub.add_parser("research", help="Run research on a single provider")
    research_p.add_argument("--provider", required=True, choices=ALL_PROVIDERS)
    research_p.add_argument("--prompt-file", required=True, help="Path to prompt file")
    research_p.add_argument("--session-dir", required=True, help="Path to session directory")

    validate_p = sub.add_parser("validate", help="Validate citations from collected reports")
    validate_p.add_argument("--session-dir", required=True, help="Path to session directory")
    validate_p.add_argument("--depth", type=int, default=0, choices=[0, 1, 2, 3])

    orchestrate_p = sub.add_parser("orchestrate", help="Run full research pipeline for a session")
    orchestrate_p.add_argument("--session-dir", required=True, help="Path to session directory (must contain prompt.md)")
    orchestrate_p.add_argument("--depth", type=int, default=0, choices=[0, 1, 2, 3], help="Citation validation depth")

    args = parser.parse_args(argv)
    config = Config.from_env()

    if args.command == "check-providers":
        _cmd_check_providers(config)
    elif args.command == "research":
        _cmd_research(args, config)
    elif args.command == "validate":
        _cmd_validate(args, config)
    elif args.command == "orchestrate":
        _cmd_orchestrate(args, config)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

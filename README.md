# Giga Research

Multi-provider deep research orchestration for Claude Code. Dispatch research prompts to Claude, OpenAI, and Gemini in parallel, then reconcile the results into one authoritative report with citation validation.

## How It Works

```
Prompt Craft → Provider Check → Parallel Dispatch → Reconcile & Validate → Report
```

1. **Prompt Craft** — Build a structured research prompt through conversation
2. **Provider Check** — Detect which API keys are configured, offer manual fallback for missing providers
3. **Dispatch** — Launch deep research on all available providers simultaneously
4. **Reconcile** — Cross-compare findings, classify agreement levels, validate citations
5. **Report** — Output a unified report, comparison matrix, and citation audit trail

Each provider uses its native deep research capability:

| Provider | API | Model |
|----------|-----|-------|
| Claude | Messages API | claude-sonnet-4-5-20250929 |
| OpenAI | Responses API (background) | o3-deep-research |
| Gemini | Interactions API (background) | deep-research-pro-preview-12-2025 |

## Quick Start

### 1. Clone and install

```bash
git clone <repo-url> giga-research-skill
cd giga-research-skill
uv sync --extra dev
```

Requires Python 3.11+ and [uv](https://docs.astral.sh/uv/).

### 2. Configure API keys

Copy the example env file and fill in your keys:

```bash
cp .env.example .env
```

Edit `.env`:

```env
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=AI...
```

The skill works with **any subset** of these keys (minimum 1). Missing providers can be handled via manual fallback during a research session.

Environment variables, if already set in your shell, take precedence over `.env` values.

### 3. Verify setup

```bash
uv run python -m giga_research.cli check-providers
```

Expected output (with all keys configured):

```
Available providers: claude, openai, gemini
{"available": ["claude", "openai", "gemini"], "missing": []}
```

### 4. Use the skill

The primary interface is the `SKILL.md` file, designed to be used as a [Claude Code skill](https://docs.anthropic.com/en/docs/claude-code/skills). Add this project's directory to your Claude Code skill paths, or invoke the workflow manually by following the phases in `SKILL.md`.

## CLI Reference

The CLI is the programmatic interface used by the skill's subagents. You can also use it directly.

### check-providers

Report which API keys are configured.

```bash
uv run python -m giga_research.cli check-providers
```

### research

Run deep research on a single provider. Reads the prompt from a file and saves results to the session directory.

```bash
uv run python -m giga_research.cli research \
    --provider <claude|openai|gemini> \
    --prompt-file <path/to/prompt.md> \
    --session-dir <path/to/session-dir>
```

Results are saved to `<session-dir>/raw/<provider>.md` (markdown) and `<session-dir>/raw/<provider>.json` (structured metadata).

**Timing expectations:**
- Claude: ~1-2 minutes (synchronous completion)
- OpenAI: ~5-10 minutes (background polling at 10s intervals)
- Gemini: ~5-10 minutes (background polling at 10s intervals)

### validate

Validate citations extracted from collected research reports.

```bash
uv run python -m giga_research.cli validate \
    --session-dir <path/to/session-dir> \
    --depth <0|1|2|3>
```

Validation depths:

| Depth | What it does |
|-------|-------------|
| 0 | No validation (default) |
| 1 | URL liveness check (HEAD request) |
| 2 | Content verification (checks if cited claim exists at URL) |
| 3 | Full verification + find replacements for dead citations |

## Session Directory Structure

Each research session creates a timestamped directory under `research-output/`:

```
research-output/20260214-153012-ransomware-landscape/
├── prompt.md               # Approved research prompt
├── raw/
│   ├── claude.md           # Raw Claude output
│   ├── claude.json         # Claude metadata (model, tokens, latency)
│   ├── openai.md           # Raw OpenAI output
│   ├── openai.json
│   ├── gemini.md           # Raw Gemini output
│   └── gemini.json
├── report.md               # Unified reconciled report
├── comparison-matrix.md    # Topic × provider agreement grid
├── validation-log.md       # Citation audit trail (if depth > 0)
└── meta.json               # Session metadata
```

## Configuration

All configuration is loaded from environment variables (and the `.env` file). The `Config` class in `src/giga_research/config.py` supports:

| Variable | Default | Description |
|----------|---------|-------------|
| `ANTHROPIC_API_KEY` | — | Claude API key |
| `OPENAI_API_KEY` | — | OpenAI API key |
| `GEMINI_API_KEY` | — | Gemini API key |

Additional settings are configured in code via the `Config` model:

| Field | Default | Description |
|-------|---------|-------------|
| `request_timeout` | 900s | Per-request timeout (deep research can take 5-10 min) |
| `max_retries` | 3 | Retry count with exponential backoff |
| `citation_validation_depth` | 0 | Default validation depth (0-3) |
| `output_dir` | `research-output` | Base output directory |

## Architecture

```
src/giga_research/
├── clients/
│   ├── base.py             # Abstract base with retry + timeout
│   ├── claude.py           # Anthropic Messages API
│   ├── openai_client.py    # OpenAI Responses API (deep research)
│   └── gemini.py           # Google Interactions API (deep research)
├── research/
│   ├── dispatcher.py       # Parallel asyncio.gather dispatch
│   └── collector.py        # Session directory + file management
├── validation/
│   ├── url_checker.py      # HTTP liveness + content fetch
│   └── citations.py        # Multi-depth citation validation
├── reconciliation/
│   ├── analyzer.py         # Cross-report comparison + dedup
│   └── report_builder.py   # Markdown report generation
├── output/
│   └── writer.py           # Write all session artifacts
├── cli.py                  # CLI entry point (3 subcommands)
├── config.py               # Config with .env auto-loading
├── errors.py               # Structured error hierarchy
└── models.py               # Pydantic models (Result, Citation, etc.)
```

**Key design decisions:**

- **Provider isolation** — Each client implements `_do_research()` behind a common interface. The base class handles retry logic, timeouts, and error wrapping.
- **Async-first** — All API calls use async clients. The CLI bridges sync/async via `asyncio.run()`.
- **Graceful degradation** — Missing API keys are detected early. The skill offers manual fallback (paste prompt into provider's web UI, save result to session dir).
- **Structured errors** — `ProviderError` hierarchy (`ProviderTimeoutError`, `ProviderRateLimitError`) enables the base client to make smart retry decisions.

## Development

### Run tests

```bash
uv run pytest -v
```

71 tests covering all modules. Tests mock external API calls — no API keys needed to run the suite.

### Lint and format

```bash
uv run ruff check src/ tests/
uv run ruff format src/ tests/
```

Ruff is configured for Python 3.11+ with a 120-character line length.

### Add a new provider

1. Create `src/giga_research/clients/new_provider.py` implementing `BaseResearchClient`
2. Implement `is_available()` and `_do_research(prompt) -> ResearchResult`
3. Add the API key field to `Config` and `Config.from_env()`
4. Register the provider in `cli.py`'s `client_map`
5. Add tests in `tests/test_clients/test_new_provider.py`

## Manual Fallback Workflow

When an API key isn't available for a provider, the skill supports manual fallback:

1. Open the provider's deep research web interface (e.g., ChatGPT, Gemini, Claude)
2. Paste the contents of `<session-dir>/prompt.md`
3. Wait for the deep research to complete
4. Save the output to `<session-dir>/raw/<provider>.md`
5. Continue with reconciliation

## License

Apache 2.0 — see [LICENSE](LICENSE).

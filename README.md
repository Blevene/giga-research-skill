# Giga Research

Multi-provider deep research orchestration for Claude Code. Dispatch research prompts to Claude, OpenAI, and Gemini in parallel, then reconcile the results into one authoritative report with citation validation.

## How It Works

```
Prompt Craft → Setup + Launch → Coordinator Subagent → Report
```

1. **Prompt Craft** — Build a structured research prompt through conversation
2. **Setup + Launch** — Detect providers, create session, launch a single background coordinator
3. **Coordinator** — Runs the full pipeline (dispatch → validate → compare), then synthesizes a unified report
4. **Report** — Unified report, comparison matrix, and citation audit trail delivered back to main conversation

Each provider uses its native deep research capability:

| Provider | API | Model |
|----------|-----|-------|
| Claude | Messages API + Web Search | claude-sonnet-4-6 |
| OpenAI | Responses API (background) | o3-deep-research |
| Gemini | Interactions API (background) | deep-research-pro-preview-12-2025 |

## Installation

Requires Python 3.11+.

### 1. Install with pip

```bash
# All providers
pip install "giga-research[all]"

# Or pick only the providers you need
pip install "giga-research[claude]"
pip install "giga-research[claude,openai]"
pip install "giga-research[gemini]"
```

### 1a. Install with uv (recommended)

```bash
# All providers
uv add "giga-research[all]"

# Or pick only the providers you need
uv add "giga-research[claude,openai]"
```

### 1b. Install from source (for development)

```bash
git clone <repo-url> giga-research-skill
cd giga-research-skill
uv sync --extra dev
```

This installs all provider SDKs plus dev tools (pytest, ruff).

> **Skill users:** If you're using this as a Claude Code skill, you don't need to run `uv sync` manually. All CLI commands use `uv run --project <path>` which auto-creates the venv and installs deps on first run.

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

Where to get each key:

| Provider | Where to get your key | Required plan |
|----------|----------------------|---------------|
| Claude | [console.anthropic.com/settings/keys](https://console.anthropic.com/settings/keys) | Any paid plan |
| OpenAI | [platform.openai.com/api-keys](https://platform.openai.com/api-keys) | Plus or Team (deep research requires o3 access) |
| Gemini | [aistudio.google.com/apikey](https://aistudio.google.com/apikey) | Free tier works, but deep research may require paid |

The skill works with **any subset** of these keys (minimum 1). Missing providers can be handled via manual fallback during a research session.

Environment variables, if already set in your shell, take precedence over `.env` values. You can also export keys directly in your shell profile instead of using `.env`:

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
export OPENAI_API_KEY="sk-..."
export GEMINI_API_KEY="AI..."
```

### 3. Verify setup

```bash
giga-research check-providers
```

Expected output (with all keys configured):

```
Available providers: claude, openai, gemini
{"available": ["claude", "openai", "gemini"], "missing": []}
```

> **Note:** If you installed from source with `uv sync`, use `uv run giga-research` instead of `giga-research`.

### 4. Add as a Claude Code skill

The primary interface is the `SKILL.md` file, designed to be used as a [Claude Code skill](https://docs.anthropic.com/en/docs/claude-code/skills).

Point Claude Code at the project directory. The simplest way is to add it to your project's `.claude/settings.json`:

```json
{
  "permissions": {
    "allow": [],
    "deny": []
  },
  "skills": ["/path/to/giga-research-skill"]
}
```

Or symlink it into your global skills directory for access from any project:

```bash
ln -s /path/to/giga-research-skill ~/.claude/skills/giga-research
```

Then invoke the skill by asking Claude Code to do deep research — it will pick up the `SKILL.md` workflow automatically.

## CLI Reference

The CLI is the programmatic interface used by the skill's subagents. You can also use it directly.

### check-providers

Report which API keys are configured.

```bash
giga-research check-providers
```

### create-session

Create a timestamped session directory for a research topic.

```bash
giga-research create-session --topic <topic-slug> [--output-dir <path>]
```

Prints the absolute path of the created session directory. Defaults to `<skill-root>/research-output/` if `--output-dir` is not specified.

### research

Run deep research on a single provider. Reads the prompt from a file and saves results to the session directory.

```bash
giga-research research \
    --provider <claude|openai|gemini> \
    --prompt-file <path/to/prompt.md> \
    --session-dir <path/to/session-dir>
```

Results are saved to `<session-dir>/raw/<provider>.md` (markdown) and `<session-dir>/raw/<provider>.json` (structured metadata).

**Timing expectations:**
- Claude: ~1-2 minutes (synchronous completion)
- OpenAI: ~5-10 minutes (background polling at 10s intervals)
- Gemini: ~5-10 minutes (background polling at 10s intervals)

### orchestrate

Run the full deterministic pipeline for a session: dispatch all available providers in parallel, validate citations, build comparison matrix, and save all structural outputs.

```bash
giga-research orchestrate \
    --session-dir <path/to/session-dir> \
    --depth <0|1|2|3>
```

Expects `<session-dir>/prompt.md` to already exist. Outputs a JSON summary to stdout:

```json
{
  "session_dir": "research-output/20260214-153012-ransomware-landscape",
  "providers_used": ["claude", "openai", "gemini"],
  "providers_failed": {},
  "citation_count": 42,
  "citations_validated": 0,
  "topics_identified": ["Threat Landscape", "Key Actors", "Defenses"]
}
```

This is the command the coordinator subagent uses internally. It handles all deterministic work — the coordinator only adds LLM synthesis for the unified `report.md`.

### validate

Validate citations extracted from collected research reports.

```bash
giga-research validate \
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
├── comparison-matrix.md    # Topic x provider agreement grid
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
├── orchestration/
│   └── pipeline.py         # Full pipeline: dispatch → validate → compare
├── clients/
│   ├── base.py             # Abstract base with retry + timeout
│   ├── claude.py           # Anthropic Messages API + web search citations
│   ├── openai_client.py    # OpenAI Responses API (deep research)
│   └── gemini.py           # Google Interactions API (deep research)
├── research/
│   ├── dispatcher.py       # Parallel dispatch with streaming callbacks
│   ├── progress.py         # Progress event dataclasses + callback type
│   └── collector.py        # Session directory + file management
├── validation/
│   ├── url_checker.py      # HTTP liveness + content fetch
│   └── citations.py        # Multi-depth citation validation
├── reconciliation/
│   ├── analyzer.py         # Cross-report comparison + dedup
│   └── report_builder.py   # Markdown report generation
├── output/
│   └── writer.py           # Write all session artifacts
├── cli.py                  # CLI entry point (5 subcommands)
├── config.py               # Config with .env auto-loading
├── errors.py               # Structured error hierarchy
└── models.py               # Pydantic models (Result, Citation, etc.)
```

**Key design decisions:**

- **Coordinator pattern** — Post-prompt-approval, the entire workflow runs inside a single background subagent. The `orchestrate` command handles all deterministic work (dispatch, validate, compare); the coordinator subagent adds LLM synthesis for the unified report. This keeps the main conversation clean.
- **Provider isolation** — Each client implements `_do_research()` behind a common interface. The base class handles retry logic, timeouts, and error wrapping.
- **Async-first** — All API calls use async clients. The CLI bridges sync/async via `asyncio.run()`.
- **Graceful degradation** — Missing API keys are detected early. Failed providers don't block others. The skill offers manual fallback (paste prompt into provider's web UI, save result to session dir).
- **Structured errors** — `ProviderError` hierarchy (`ProviderTimeoutError`, `ProviderRateLimitError`) enables the base client to make smart retry decisions.

## Development

### Run tests

```bash
uv run pytest -v
```

104 tests covering all modules. Tests mock external API calls — no API keys needed to run the suite.

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
4. Add an entry to `CLIENT_REGISTRY` in `config.py` (`ALL_PROVIDERS` derives from it automatically)
5. Add an optional dependency group in `pyproject.toml` (e.g., `newprovider = ["newprovider-sdk>=1.0"]`) and include it in the `all` extra
6. Add tests in `tests/test_clients/test_new_provider.py`

## Manual Fallback Workflow

When an API key isn't available for a provider, the skill supports manual fallback:

1. Open the provider's deep research web interface (e.g., ChatGPT, Gemini, Claude)
2. Paste the contents of `<session-dir>/prompt.md`
3. Wait for the deep research to complete
4. Save the output to `<session-dir>/raw/<provider>.md`
5. Continue with reconciliation

## License

Apache 2.0 — see [LICENSE](LICENSE).

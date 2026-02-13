# Giga Research Skill — Design Document

**Date:** 2026-02-13
**Status:** Approved

## Overview

A standalone Claude Code skill that orchestrates multi-provider deep research. One monolithic SKILL.md handles workflow orchestration, backed by a Python package (`giga_research`) for API interactions, citation validation, and report assembly.

The skill automates a common manual workflow: crafting a research prompt, dispatching it to multiple AI research providers in parallel, then analyzing, critiquing, and reconciling the results into a single authoritative report.

## Architecture

### Project Structure

```
giga-research-skill/
├── SKILL.md                          # Skill orchestration logic
├── pyproject.toml                    # uv + modern Python packaging
├── uv.lock                           # Lockfile
├── src/
│   └── giga_research/
│       ├── __init__.py
│       ├── config.py                 # Env var loading, validation, settings
│       ├── cli.py                    # CLI interface for subagent invocation
│       ├── clients/
│       │   ├── __init__.py
│       │   ├── base.py              # Abstract base client (retry, timeout, rate limit)
│       │   ├── claude.py            # Claude API (Anthropic SDK)
│       │   ├── openai.py            # OpenAI API (openai SDK)
│       │   └── gemini.py            # Gemini API (google-genai SDK)
│       ├── research/
│       │   ├── __init__.py
│       │   ├── dispatcher.py        # Parallel dispatch orchestration
│       │   └── collector.py         # Result collection, normalization
│       ├── validation/
│       │   ├── __init__.py
│       │   ├── citations.py         # Citation validation (levels 0-3)
│       │   └── url_checker.py       # URL liveness + content fetch
│       ├── reconciliation/
│       │   ├── __init__.py
│       │   ├── analyzer.py          # Cross-report analysis
│       │   └── report_builder.py    # Unified report assembly
│       └── output/
│           ├── __init__.py
│           └── writer.py            # Structured markdown output
└── tests/
    ├── conftest.py
    ├── test_clients/
    ├── test_validation/
    └── test_reconciliation/
```

### Key Decisions

- **Monolithic SKILL.md** — single file orchestrates the entire workflow as a linear state machine with clear phase gates
- **Python package via uv** — modern packaging with lockfile, `>=3.11`
- **Subagents for parallelism** — `Task` tool launches parallel research and validation
- **CLI interface** — subagents invoke `uv run python -m giga_research.cli <command>` rather than writing inline Python
- **Graceful degradation** — runs with whatever API keys are available, manual fallback for the rest

## Workflow Phases

### Phase 1: Prompt Craft

- Conversational refinement: skill asks about topic, scope, depth one question at a time
- Builds structured prompt with: topic, scope boundaries, specific questions, desired depth, output expectations
- **Gate:** User must approve the prompt before proceeding

### Phase 2: Provider Check

- Runs `giga_research.cli check-providers` to detect available API keys
- Reports which providers are available vs missing
- For missing providers: asks user to skip or use manual fallback
- Creates session directory: `research-output/<timestamp>-<slug>/`

### Phase 3: Dispatch Research

- One subagent per available provider, launched in parallel via multiple `Task` calls
- Each subagent runs: `uv run python -m giga_research.cli research --provider <name> --prompt-file <path>`
- Results written to `research-output/<session>/raw/<provider>.md`
- Manual fallback: writes prompt to `prompt.md`, user pastes result into the expected file
- **Gate:** All results (API + manual) must be collected before proceeding

### Phase 4: Reconcile & Validate

- Asks user for citation validation depth (0-3, default 0)
- Subagent runs citation validation: `uv run python -m giga_research.cli validate --session <path> --depth <N>`
- Reconciliation subagent performs:
  1. Structural analysis — parse reports into topic map
  2. Consensus/conflict detection — classify claims as consensus, majority, contested, or unique
  3. Citation cross-reference — deduplicate, corroborate, validate
  4. Synthesis — write unified narrative

### Phase 5: Output Report

Writes all artifacts to `research-output/<session>/`.

## Python Package Design

### Core Types

```python
class ResearchResult(BaseModel):
    provider: str                    # "claude" | "openai" | "gemini"
    content: str                     # Raw research output (markdown)
    citations: list[Citation]        # Extracted citations
    metadata: ResultMetadata         # Tokens, latency, model version

class Citation(BaseModel):
    text: str                        # The claim being cited
    url: str | None                  # Source URL
    title: str | None                # Source title
    validation_status: ValidationStatus = ValidationStatus.UNCHECKED

class ValidationStatus(str, Enum):
    UNCHECKED = "unchecked"
    ALIVE = "alive"
    DEAD = "dead"
    VERIFIED = "verified"
    HALLUCINATED = "hallucinated"
    REPLACED = "replaced"
```

### Base Client

Abstract base with:
- Retry: exponential backoff with jitter, max 3 retries
- Rate limiting: token bucket, respects provider API headers
- Timeout: 300s default (research tasks are slow)
- Response validation: Pydantic models per provider

Each provider client (`claude.py`, `openai.py`, `gemini.py`) wraps its official SDK and normalizes responses into `ResearchResult`.

### Config

```python
class Config(BaseModel):
    claude_api_key: str | None = Field(default=None, repr=False)
    openai_api_key: str | None = Field(default=None, repr=False)
    gemini_api_key: str | None = Field(default=None, repr=False)
    request_timeout: int = 300
    max_retries: int = 3
    citation_validation_depth: int = 0
    output_dir: Path = Path("research-output")
```

- Keys loaded only from environment variables
- `repr=False` on secrets — never appear in logs/tracebacks
- Pydantic validation at startup

### Citation Validation Levels

| Level | Behavior |
|-------|----------|
| 0 | No validation |
| 1 | URL liveness check (HTTP HEAD) |
| 2 | Content verification (fetch + check claim exists in source) |
| 3 | Full verification + web search for replacement sources |

- `asyncio.Semaphore`-bounded concurrent requests (max 10)
- Uses `httpx` async client

### Dispatcher

- `asyncio.gather` with `return_exceptions=True` — one provider failing doesn't kill others
- Returns dict mapping provider name to result or structured error

### CLI Commands

```
check-providers    Report which API keys are configured
research           Run research on a single provider
validate           Validate citations from collected reports
reconcile          Build comparison matrix from raw reports
```

### Dependencies

```toml
[project]
requires-python = ">=3.11"
dependencies = [
    "anthropic>=0.40",
    "openai>=1.50",
    "google-genai>=1.0",
    "httpx>=0.27",
    "pydantic>=2.0",
]

[project.optional-dependencies]
dev = ["pytest>=8.0", "pytest-asyncio>=0.24", "respx>=0.22", "ruff>=0.8"]
```

## Error Handling

| Failure | Behavior |
|---------|----------|
| API key missing | Skip provider, offer manual fallback |
| API timeout (300s) | Retry once with 600s timeout, then manual fallback |
| API rate limit | Backoff and retry (up to 3 attempts) |
| API returns error | Log error, offer manual fallback |
| Malformed response | Log validation error, offer manual fallback |
| Citation URL dead | Flag in validation log, find replacement at depth 3 |
| All providers fail | Skill halts, explains what happened, suggests manual approach |

Pattern: never silently fail, always give the user a clear path forward.

## Output Artifacts

All written to `research-output/<timestamp>-<slug>/`:

| File | Contents |
|------|----------|
| `report.md` | Unified synthesized report (executive summary, findings by topic, disagreements, gaps, references, confidence annotations) |
| `comparison-matrix.md` | Topic x Provider grid with agreement/disagreement per cell |
| `validation-log.md` | Citation audit trail (if depth > 0) |
| `raw/claude.md` | Original Claude report |
| `raw/openai.md` | Original OpenAI report |
| `raw/gemini.md` | Original Gemini report |
| `prompt.md` | The research prompt used |
| `meta.json` | Session metadata (providers, timestamps, config, token usage) |

## Safety Practices

- API keys via environment variables only, `repr=False` on all secret fields
- Rate limiting per provider with token bucket
- Retry with exponential backoff and jitter
- Input sanitization on user-provided topic/scope
- Structured error handling — typed exceptions, never bare `except`
- Timeout guards on all network requests
- Pydantic response validation on all API responses
- Semaphore-bounded concurrent URL fetching during citation validation

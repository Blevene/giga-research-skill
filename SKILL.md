---
name: giga-research
description: Orchestrate multi-provider deep research with parallel dispatch, citation validation, and reconciled report output.
---

# Giga Research

## Overview

Orchestrate deep research across Claude, OpenAI, and Gemini in parallel. Craft a research prompt conversationally, then launch a single background coordinator that dispatches providers, validates citations, and synthesizes a unified report — all without polluting the main conversation.

## Prerequisites

This skill requires the `giga_research` Python package. Before starting:

```bash
cd <path-to-giga-research-skill>
uv sync
```

API keys are loaded automatically from a `.env` file in the skill folder root:

```bash
cp .env.example .env
# Edit .env and fill in your API keys
```

Supported keys:
- `ANTHROPIC_API_KEY` — for Claude
- `OPENAI_API_KEY` — for OpenAI
- `GEMINI_API_KEY` — for Gemini (uses Deep Research via Interactions API)

The skill works with any subset of these (minimum 1). Environment variables, if already set, take precedence over the `.env` file.

## Workflow

```dot
digraph workflow {
    rankdir=TB;
    "Phase 1: Prompt Craft" [shape=box];
    "User approves prompt?" [shape=diamond];
    "Phase 2: Setup + Launch" [shape=box];
    "Coordinator Subagent" [shape=box, style=filled, fillcolor=lightblue];
    "Done" [shape=doublecircle];

    "Phase 1: Prompt Craft" -> "User approves prompt?";
    "User approves prompt?" -> "Phase 1: Prompt Craft" [label="revise"];
    "User approves prompt?" -> "Phase 2: Setup + Launch" [label="approved"];
    "Phase 2: Setup + Launch" -> "Coordinator Subagent";
    "Coordinator Subagent" -> "Done" [label="returns summary"];
}
```

---

## Phase 1: Prompt Craft

**Goal:** Build a well-structured research prompt through conversation.

1. Ask the user about their research topic. One question at a time.
2. Clarify: scope boundaries, specific questions to answer, desired depth, output expectations.
3. Build a structured prompt incorporating all of the above.
4. Present the full prompt to the user for approval.
5. **GATE:** Do NOT proceed until the user explicitly approves the prompt.

The prompt should follow this structure:
```
# Research Task: [Topic]

## Scope
[What to include and exclude]

## Key Questions
1. [Specific question]
2. [Specific question]
...

## Depth & Focus
[How deep to go, what to prioritize]

## Output Expectations
[Structure, length, citation requirements]
```

---

## Phase 2: Setup + Launch

After the user approves the prompt:

1. Run: `uv run python -m giga_research.cli check-providers`
2. Report to the user which providers are available and which are missing.
3. For each missing provider, ask: **skip** or **manual fallback**?
4. Create the session directory:
   ```bash
   uv run python -c "
   from giga_research.research.collector import create_session_dir
   from pathlib import Path
   d = create_session_dir(Path('research-output'), '<topic-slug>')
   print(d)
   "
   ```
5. Save the approved prompt to `<session-dir>/prompt.md`.
6. Ask the user for citation validation depth (0-3):
   - **0** — No validation (default, fastest)
   - **1** — URL liveness check
   - **2** — Content verification (checks if cited claim exists in source)
   - **3** — Full verification + find replacements for dead citations
7. **Launch the coordinator subagent** as a single background Task using the prompt template below.
8. Tell the user: "Research is running in the background. I'll report back when it's done."

**For manual fallback providers** (if any):
1. Before launching the coordinator, tell the user: "Please paste the prompt from `<session-dir>/prompt.md` into [Provider]'s deep research interface."
2. Ask them to save the result to `<session-dir>/raw/<provider>.md`
3. Wait for confirmation, then launch the coordinator.

---

## Coordinator Subagent Instructions

**Launch ONE background subagent** using the Task tool with the following prompt template. Replace `<session-dir>` and `<depth>` with actual values.

```
You are a research coordinator. Your job is to run the research pipeline, then synthesize a unified report.

## Step 1: Run the pipeline

Run this command:
```bash
uv run python -m giga_research.cli orchestrate \
    --session-dir <session-dir> \
    --depth <depth>
```

Parse the JSON output. It will contain:
- providers_used: which providers returned results
- providers_failed: which providers failed (with error messages)
- citation_count: total citations found
- citations_validated: how many were validated
- topics_identified: list of topics from cross-report analysis

If all providers failed, report this back and stop.

## Step 2: Read the generated files

Read these files from <session-dir>:
- raw/<provider>.md for each provider in providers_used
- comparison-matrix.md
- validation-log.md (if depth > 0)

## Step 3: Synthesize unified report

Using the raw reports and comparison matrix, write <session-dir>/report.md with this structure:

```markdown
# [Topic] — Research Report

## Executive Summary
[2-3 paragraph synthesis of key findings]

## Methodology
Synthesized from research conducted via: [list providers used].
Citation validation depth: [N].

## Findings
### [Topic 1]
[Synthesized findings. Tag sources: [Claude, OpenAI], [Gemini only], etc.]
[Classify each claim:]
- **Consensus** — all sources agree (high confidence)
- **Majority** — 2 of 3 agree (note the dissent)
- **Contested** — sources disagree (present all perspectives)
- **Unique** — only one source covers it (note single-source)

### [Topic 2]
...

## Areas of Disagreement
[Explicit section for contested claims with all perspectives]

## Gaps & Limitations
[What none of the sources covered adequately]

## References
[Deduplicated, validated citation list]
```

## Step 4: Return summary

Report back with:
1. Which providers succeeded/failed
2. Number of topics identified
3. Number of citations found and validated
4. Any notable findings (high disagreement, dead citations, unique insights)
5. The path to report.md as the primary deliverable
6. Paths to all output files in the session directory
```

---

## Session Output

The coordinator produces these files in `<session-dir>/`:
- `report.md` — unified synthesized report (written by coordinator)
- `comparison-matrix.md` — topic x provider grid (written by pipeline)
- `validation-log.md` — citation audit trail (written by pipeline)
- `raw/<provider>.md` — original provider reports (written by pipeline)
- `raw/<provider>.json` — full result with metadata (written by pipeline)
- `prompt.md` — the research prompt (written by parent in Phase 2)
- `meta.json` — session metadata with timing/tokens (written by pipeline)

---

## Error Handling

- If a provider API call fails: the pipeline isolates the failure and continues with remaining providers. The coordinator reports which providers failed.
- If all providers fail: the coordinator reports the errors. The parent agent should inform the user and suggest manual fallback.
- Never silently skip a failure. Always inform the user and offer a path forward.

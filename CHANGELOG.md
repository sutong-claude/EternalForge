# Changelog

## 0.6.0 — 2026-09-14

- Second live SearchAdapter: DuckDuckGo Instant Answer (`DuckDuckGoAdapter`).
- `get_adapter(name)` factory; CLI `--backend wikipedia|duckduckgo|fixture` on `research` and `capture`.
- Payload parsers covered by tests without hitting the network.

## 0.5.0 — 2026-09-14

- Research hits persist to `memory/journal.jsonl` via `tools.research.record_hits`.
- CLI `research` writes `kind=research` entries unless `--no-journal`.
- Tests for journaled hits and empty-result entries.

## 0.4.1 — 2026-09-14

- Planner skips blank, whitespace-only, and "None yet" priorities.
- Empty queue returns FALLBACK instead of an empty string.
- Added `tests/test_planner.py` covering empty, placeholder, strip, parse-round-trip, and post-complete cases.

## 0.4.0 — 2026-09-14

- Cycle changelog + metrics: `core.changelog.append_entry` and `core.metrics.bump_metrics`.
- `Agent.reflect` writes CHANGELOG.md, recounts Files/Tests, increments Cycles.
- Tests for version bump, changelog prepend, metrics recount, and live cycle side-effects.

## 0.3.0 — 2026-09-14

- Daily knowledge capture: `tools.capture.capture()` writes `memory/YYYY-MM-DD.md`.
- CLI: `eternalforge capture [--topic T] [--offline] [--day YYYY-MM-DD]`.
- Journal entries with `kind=capture`.
- Tests for markdown output, append-same-day, and invalid date keys.

## 0.2.0 — 2026-09-14

- Research tool: `SearchAdapter` protocol, `FixtureAdapter`, `WikipediaAdapter`.
- CLI: `eternalforge research QUERY [--offline] [--max N]`.
- Tests for fixture search, truncation, and formatting.

## 0.1.0 — 2026-09-14

- Living STATE.md protocol with parse/dump round-trip.
- JSONL memory journal.
- Planner that selects a single next task.
- CLI: `status`, `next`, `cycle --dry-run`.
- Hourly automation contract documented in AGENTS.md.

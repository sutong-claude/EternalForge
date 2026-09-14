# Changelog

## 0.4.0 — 2026-09-14

- Cycle changelog + metrics: `core.changelog.append_entry` and `core.metrics.bump_metrics`.
- `Agent.reflect` writes CHANGELOG.md, recounts Files/Tests, increments Cycles, journals the version.
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

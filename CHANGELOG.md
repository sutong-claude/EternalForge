# Changelog

## 0.8.2 — 2026-09-15

- KB query filters: `search_kb` / `search_index` accept `kind`, `since`, `until`.
- Markdown notes dated from `YYYY-MM-DD.md`; journal rows use entry timestamps.
- CLI: `eternalforge kb QUERY [--kind K] [--since YYYY-MM-DD] [--until YYYY-MM-DD]`.
- Undated documents are excluded when a date range is set; invalid dates raise ValueError.

## 0.8.1 — 2026-09-15

- Journal kind filter: `Journal.recent` / `recent_kinds` accept `kind=` (case-insensitive).
- `Journal.format_recent` dumps timestamp/kind/summary[/details].
- CLI: `eternalforge recent [--kind K] [--max N]` and `eternalforge status --kind K`.
- Status prints `journal_filter=` when a kind is requested.

## 0.8.0 — 2026-09-15

- Knowledge-base index over `memory/*.md` and `memory/journal.jsonl`.
- `tools.kb`: `collect_documents`, `build_index`, `search_kb`, optional `memory/kb-index.json`.
- CLI: `eternalforge kb QUERY [--max N] [--write-index]`.
- Tests cover tokenize, mixed sources, bad JSONL, ranking, and snapshot write.

## 0.7.0 — 2026-09-14

- Third live SearchAdapter: Open Library (`OpenLibraryAdapter`, `parse_openlibrary_payload`).
- Multi-backend search: `merge_hits` (round-robin, URL/title dedupe, drop unavailable placeholders) and `MultiAdapter`.
- CLI `--backend wikipedia|duckduckgo|openlibrary|multi|fixture` (aliases: ddg, ol, books, all).
- Payload / merge tests do not hit the network.

## 0.6.3 — 2026-09-14

- `eternalforge status` prints `journal_kinds=` from the last JSONL entries.
- `Journal.recent_kinds` / `format_recent_kinds`; skip blank kinds and bad JSON lines.
- Tests for empty journal, window limit, and status wiring after a cycle.

## 0.6.2 — 2026-09-14

- Harden STATE progress parsing: single `parse_progress` helper (no duplicate try-blocks).
- Accepts ``34%``, ``34 percent``, bare ``34``, or fraction ``0.34``; clamps to [0, 1].
- Tests for percent/fraction/invalid/clamped values and STATE field wiring.

## 0.6.1 — 2026-09-14

- Count CHANGELOG `## X.Y.Z` headings via `count_versions` / `count_versions_file`.
- `eternalforge status` prints `changelog_versions=N`.
- Tests for missing file, non-semver headings, and status line.

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

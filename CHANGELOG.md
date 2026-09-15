# Changelog

## 0.11.3 — 2026-09-15

- Task list sort by due (default) or priority; undated tasks sink to the end.
- Overdue flag: open tasks with `due` before today; `list_tasks(..., overdue=True)`.
- CLI: `task list [--overdue] [--sort due|priority]`.
- `format_tasks` prints `OVERDUE` after status when the due date has passed.

## 0.11.2 — 2026-09-15

- Task due dates and priority on `memory/tasks.jsonl`.
- `normalize_due` (YYYY-MM-DD) and `normalize_priority` (low/medium/high/urgent; aliases p0–p3).
- `update_task` sets status / due / priority; `set_task_status` remains a thin wrapper.
- CLI: `task add --due --priority`, `task list --priority`, `task set ID [STATUS] [--due] [--priority]`.
- List formatting shows `p=` when not medium and `due=` when set; legacy rows default to medium / no due.

## 0.11.1 — 2026-09-15

- Persist open task count in STATE metrics on cycle (`Tasks=N`).
- `bump_metrics` recounts `memory/tasks.jsonl` via `count_open_tasks` when a workspace root is given.
- Done / cancelled tasks are excluded; missing store → 0.
- Tests cover no-root skip, empty store, open-only count, and cycle write-back.

## 0.11.0 — 2026-09-15

- Task-tracking skeleton: JSONL store at `memory/tasks.jsonl` (`tools.tasks`).
- Add / list / set status helpers; ids increment as T001, T002, …
- Status aliases: todo→open, completed→done, canceled→cancelled.
- CLI: `eternalforge task add TITLE [--tag] [--notes]`, `task list [--status]`, `task done ID`, `task set ID STATUS`.
- Journal rows with `kind=task`; `eternalforge status` prints `tasks=N` (open count).

## 0.10.1 — 2026-09-15

- Journal dump filter by persisted tag: `Journal.recent` / `format_recent` accept `tag=`.
- Match is case-insensitive and strips a leading `#`.
- CLI: `eternalforge recent [--kind K] [--tag T] [--max N]`.
- Empty dump names both filters (`kind=` and `tag=`).

## 0.10.0 — 2026-09-15

- Fifth live SearchAdapter: arXiv via the export Atom API (`ArxivAdapter`, `parse_arxiv_payload`, `parse_arxiv_xml`).
- CLI `--backend arxiv` (aliases: papers, preprint).
- `MultiAdapter` now includes arXiv as a fifth live source.
- Payload / Atom XML tests do not hit the network.

## 0.9.2 — 2026-09-15

- Persist journal `tags` on `MemoryEntry` writes (`normalize_tags`, JSONL field).
- Capture / research / report / cycle rows store kind plus optional extra tags.
- CLI: `research|capture|report --tag T` (repeatable).
- `Journal.format_recent` prints `#tags`; legacy rows without the field load as `[]`.

## 0.9.1 — 2026-09-15

- Persist compiled report count in STATE metrics on cycle (`Reports=N`).
- `bump_metrics` recounts `memory/reports/*.md` via `count_reports` when a workspace root is given.
- Tests cover missing reports dir, markdown-only count, and cycle write-back.

## 0.9.0 — 2026-09-15

- Fourth live SearchAdapter: Hacker News via Algolia (`HackerNewsAdapter`, `parse_hackernews_payload`).
- CLI `--backend hackernews` (aliases: hn, algolia).
- `MultiAdapter` now includes HN as a fourth live source.
- Payload tests do not hit the network.

## 0.8.6 — 2026-09-15

- Surface compiled research report count in `eternalforge status` as `reports=N`.
- `tools.report.count_reports` counts `memory/reports/*.md` (missing dir → 0; ignore non-markdown).
- Tests for missing directory, markdown-only counting, and status wiring.

## 0.8.5 — 2026-09-15

- Knowledge-base source and tag facets on hits.
- Extract tags from `#hashtag` tokens and `tags:` / `tag:` lines; journal rows also honor a `tags` field.
- `search_kb` / `search_index` / `document_matches` accept `source` and `tag`.
- CLI: `eternalforge kb QUERY [--source S] [--tag T]`.
- Hit formatting shows `src=` when it differs from kind, plus `#tags`.

## 0.8.4 — 2026-09-15

- Knowledge base indexes `memory/reports/*.md` as `kind=report` / `source=report`.
- Document ids use the repo-relative path (`md:memory/reports/…`) so daily notes and reports do not collide.
- `eternalforge kb QUERY --kind report` filters compiled research reports.
- Tests cover report collection, kind filter, and a missing reports directory.

## 0.8.3 — 2026-09-15

- Automated research report from journal `kind=research` hits (`tools.report`).
- Groups runs by query parsed from `Research '…': N hit(s)` summaries.
- Writes `memory/reports/YYYY-MM-DD.md` and a `kind=report` journal row.
- CLI: `eternalforge report [--day] [--since] [--until] [--max]`.

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

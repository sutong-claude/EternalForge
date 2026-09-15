# EternalForge Live State

**Last updated:** 2026-09-15 21:05 UTC
**Current phase:** Core Agent
**Overall progress:** 73%

## Current Goal
Build a solid, self-documenting foundation for a personal AI research & development platform that can grow indefinitely through hourly autonomous improvements.

## Immediate Priorities (next few runs)
1. Optional: daily/weekly review sketch from journal + tasks
2. Optional: seventh SearchAdapter (Semantic Scholar / PubMed)
3. Optional: task title edit on `task set`

## Recent Actions
- [2026-09-15 21:05 UTC] Task set notes + tags: `update_task(..., notes=, tags=)` replaces notes/tags when provided (empty clears); CLI `task set ID [--notes] [--tag T]`; journal records notes/tag bits.
- [2026-09-15 20:12 UTC] Sixth SearchAdapter: Crossref works API (`CrossrefAdapter` / `parse_crossref_payload`); aliases doi/works; MultiAdapter includes Crossref; CLI `--backend crossref`.
- [2026-09-15 19:10 UTC] Task list tag + due-soon: `list_tasks(..., tag=, due_soon=)`; `Task.matches_tag` / `is_due_soon`; CLI `task list [--tag T] [--due-soon [N]]`; format prints `DUE-SOON`.
- [2026-09-15 18:05 UTC] CHANGELOG cycle extras: `cycle_extras(reports=, tasks=)` bullets; `Agent.reflect` appends `reports=N` / `tasks=N` after the cycle result.
- [2026-09-15 17:15 UTC] Task list sort + overdue: `sort_tasks` / `Task.sort_key` / `Task.is_overdue`; `list_tasks(..., overdue=, sort=)`; CLI `task list [--overdue] [--sort due|priority]`; format prints `OVERDUE`.
- [2026-09-15 16:10 UTC] Task due dates + priority: `due` (YYYY-MM-DD) and `priority` (low/medium/high/urgent) on Task JSONL; `normalize_due` / `normalize_priority`; `update_task`; CLI `--due` / `--priority` on add/list/set.
- [2026-09-15 15:35 UTC] Persist Tasks=N in STATE metrics: `bump_metrics` recounts open tasks via `count_open_tasks` when a workspace root is given; cycle write-back + tests.
- [2026-09-15 15:20 UTC] Task-tracking skeleton: `memory/tasks.jsonl` via `tools.tasks` (add/list/set status, T00N ids); CLI `eternalforge task add|list|done|set`; journal `kind=task`; status prints `tasks=N` open count.
- [2026-09-15 13:20 UTC] Journal recent `--tag` filter: `Journal.recent` / `format_recent` / `dump_recent` accept `tag=`; CLI `eternalforge recent [--tag T]`; case-insensitive, strips `#`.
- [2026-09-15 11:10 UTC] Fifth SearchAdapter: arXiv Atom export (`ArxivAdapter` / `parse_arxiv_payload` / `parse_arxiv_xml`); aliases papers/preprint; MultiAdapter includes arXiv; CLI `--backend arxiv`.
- [2026-09-15 10:05 UTC] Persist journal tags on MemoryEntry writes: `tags` field + `normalize_tags`; capture/research/report/cycle rows store kind (+ extras); CLI `--tag` on research/capture/report; recent dump shows `#tags`.
- [2026-09-15 09:11 UTC] Persist Reports=N in STATE metrics: `bump_metrics` recounts `memory/reports/*.md` via `count_reports` when a workspace root is given; cycle write-back + tests.
- [2026-09-15 08:15 UTC] Fourth SearchAdapter: Hacker News Algolia (`HackerNewsAdapter` / `parse_hackernews_payload`); aliases hn/algolia; MultiAdapter includes HN; CLI `--backend hackernews`.
- [2026-09-15 07:20 UTC] Tag merge dedupe: `merge_tags` + `journal_extra_tags` unique-normalize journal `tags` with `#hashtag` / `tags:` extracted tokens (order-preserving); collect_documents no longer concatenates duplicates.
- [2026-09-15 06:25 UTC] Surface report count: `tools.report.count_reports` counts `memory/reports/*.md`; `Agent.status` prints `reports=N` (missing dir → 0).
- [2026-09-15 05:05 UTC] KB source/tag facets: extract `#hashtag` and `tags:` lines; `search_kb` / `search_index` accept `source` and `tag`; CLI `eternalforge kb QUERY [--source] [--tag]`; hits print `src=` and `#tags`.

## Known Issues / Blockers
- None yet.

## Metrics
- Files: 44
- Tests: 137
- Features shipped: 32
- Cycles: 23
- Reports: 0
- Tasks: 0
- Documentation coverage: Core

## Notes for next agent
Python package is installable from pyproject.toml (package-dir = src). Run tests with: PYTHONPATH=src python -m pytest tests -q. Research/capture backends: wikipedia (default), duckduckgo, openlibrary (aliases ol/books), hackernews (aliases hn/algolia), arxiv (aliases papers/preprint), crossref (aliases doi/works), multi/all (Wikipedia + DDG + Open Library + HN + arXiv + Crossref, merged), fixture. Tests must inject FixtureAdapter / MultiAdapter(adapters=...) or call parse_*_payload helpers (no network). Implementation lives in src/tools/research.py, src/tools/openlibrary.py, src/tools/hackernews.py, src/tools/arxiv.py, and src/tools/crossref.py. Daily capture: `eternalforge capture --topic X --offline`. CLI research journals hits (`kind=research`); pass `--no-journal` to skip. Knowledge base: `eternalforge kb QUERY [--max N] [--kind K] [--source S] [--tag T] [--since YYYY-MM-DD] [--until YYYY-MM-DD] [--write-index]` indexes memory/*.md, memory/reports/*.md (kind=report), and journal.jsonl (src/tools/kb.py). Tags come from `#hashtag` tokens and `tags:` / `tag:` lines (also journal `tags` field). Journal extra_tags merge via `merge_tags` / `journal_extra_tags` (case-insensitive, # stripped, order-preserving unique). MemoryEntry now has a `tags` list persisted in JSONL (`normalize_tags` in core.memory). Writers: `record_hits` stores research + hit sources + extras; `capture` stores capture + extras; `write_report` stores report + extras; cycle rows store cycle. CLI: `research|capture|report --tag T` (repeatable). `Journal.format_recent` appends `#tag` tokens. Journal dump: `eternalforge recent [--kind K] [--tag T] [--max N]` (tag match is case-insensitive and strips `#`). Research reports: `eternalforge report [--day] [--since] [--until] [--max]` writes memory/reports/YYYY-MM-DD.md from journal research hits (src/tools/report.py) and journals kind=report. Status includes `changelog_versions`, `reports` (`count_reports` over memory/reports/*.md), `tasks` (`count_open_tasks` over memory/tasks.jsonl), `journal_kinds`, and optional `journal_filter` when `--kind` is set. Planner skips blank/None-yet entries. Progress parsing is `parse_progress` in core.state. Cycle metrics: `bump_metrics` writes `Reports=N` and `Tasks=N` (open tasks only). Cycle CHANGELOG extras include `reports=N` and `tasks=N` via `cycle_extras` in core.changelog. Task tracker: `src/tools/tasks.py` stores memory/tasks.jsonl; fields include status, notes, tags, due (YYYY-MM-DD), priority (low/medium/high/urgent, default medium). List sorts by due (undated last) or priority (urgent first); open tasks with due < today are OVERDUE; open tasks due today through N days (default 7) are DUE-SOON. CLI `eternalforge task add TITLE [--notes] [--tag T] [--due YYYY-MM-DD] [--priority P]`, `task list [--status] [--priority] [--tag T] [--overdue] [--due-soon [N]] [--sort due|priority]`, `task done ID`, `task set ID [STATUS] [--due] [--priority] [--notes] [--tag T]`; journals kind=task. `update_task` replaces notes/tags only when those kwargs are not None (empty notes/tags clear). Tag filter is case-insensitive and strips `#`; repeatable `--tag` matches any. Next: daily/weekly review sketch, seventh SearchAdapter, or task title edit on set. Keep one task per hour. Do not rewrite the protocol; extend it.

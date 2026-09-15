# EternalForge Live State

**Last updated:** 2026-09-15 11:10 UTC
**Current phase:** Core Agent
**Overall progress:** 60%

## Current Goal
Build a solid, self-documenting foundation for a personal AI research & development platform that can grow indefinitely through hourly autonomous improvements.

## Immediate Priorities (next few runs)
1. Optional: task-tracking skeleton
2. Optional: `eternalforge recent --tag` filter on persisted journal tags
3. Optional: surface Reports metric in status notes or CHANGELOG extras

## Recent Actions
- [2026-09-15 11:10 UTC] Fifth SearchAdapter: arXiv Atom export (`ArxivAdapter` / `parse_arxiv_payload` / `parse_arxiv_xml`); aliases papers/preprint; MultiAdapter includes arXiv; CLI `--backend arxiv`.
- [2026-09-15 10:05 UTC] Persist journal tags on MemoryEntry writes: `tags` field + `normalize_tags`; capture/research/report/cycle rows store kind (+ extras); CLI `--tag` on research/capture/report; recent dump shows `#tags`.
- [2026-09-15 09:11 UTC] Persist Reports=N in STATE metrics: `bump_metrics` recounts `memory/reports/*.md` via `count_reports` when a workspace root is given; cycle write-back + tests.
- [2026-09-15 08:15 UTC] Fourth SearchAdapter: Hacker News Algolia (`HackerNewsAdapter` / `parse_hackernews_payload`); aliases hn/algolia; MultiAdapter includes HN; CLI `--backend hackernews`.
- [2026-09-15 07:20 UTC] Tag merge dedupe: `merge_tags` + `journal_extra_tags` unique-normalize journal `tags` with `#hashtag` / `tags:` extracted tokens (order-preserving); collect_documents no longer concatenates duplicates.
- [2026-09-15 06:25 UTC] Surface report count: `tools.report.count_reports` counts `memory/reports/*.md`; `Agent.status` prints `reports=N` (missing dir → 0).
- [2026-09-15 05:05 UTC] KB source/tag facets: extract `#hashtag` and `tags:` lines; `search_kb` / `search_index` accept `source` and `tag`; CLI `eternalforge kb QUERY [--source] [--tag]`; hits print `src=` and `#tags`.
- [2026-09-15 04:10 UTC] KB indexes `memory/reports/*.md` as `kind=report` / `source=report`; doc ids are repo-relative (`md:memory/reports/…`); `kb QUERY --kind report` filters compiled reports.
- [2026-09-15 03:05 UTC] Research report markdown: `tools.report.write_report` groups journal `kind=research` hits by query; writes `memory/reports/YYYY-MM-DD.md`; CLI `eternalforge report [--day] [--since] [--until] [--max]`; journals `kind=report`.
- [2026-09-15 02:10 UTC] KB query filters: `search_kb` / `search_index` accept `kind`, `since`, `until`; markdown dates from `YYYY-MM-DD.md`; CLI `eternalforge kb QUERY [--kind] [--since] [--until]`.
- [2026-09-15 01:20 UTC] Journal kind filter: `Journal.recent(kind=)` + CLI `eternalforge recent [--kind] [--max]` and `status --kind`; case-insensitive match; dump timestamp/kind/summary.
- [2026-09-15 00:10 UTC] Knowledge-base index: `tools.kb` inverted index over `memory/*.md` + journal; CLI `kb QUERY`; optional `memory/kb-index.json`.
- [2026-09-14 23:15 UTC] Third SearchAdapter + merge-hits: `OpenLibraryAdapter` / `parse_openlibrary_payload`; `merge_hits` round-robin + URL dedupe; `MultiAdapter` (`--backend multi|all|openlibrary|ol|books`).
- [2026-09-14 22:15 UTC] Surface recent journal kinds in status: `Journal.recent_kinds` / `format_recent_kinds`; `Agent.status` prints `journal_kinds=...` (or `-` if empty).
- [2026-09-14 21:15 UTC] Harden STATE progress parser: `parse_progress` helper; percent/fraction/invalid/clamp; no duplicate try-blocks.

## Known Issues / Blockers
- None yet.

## Metrics
- Files: 41
- Tests: 112
- Features shipped: 23
- Cycles: 16
- Reports: 0
- Documentation coverage: Core

## Notes for next agent
Python package is installable from pyproject.toml (package-dir = src). Run tests with: PYTHONPATH=src python -m pytest tests -q. Research/capture backends: wikipedia (default), duckduckgo, openlibrary (aliases ol/books), hackernews (aliases hn/algolia), arxiv (aliases papers/preprint), multi/all (Wikipedia + DDG + Open Library + HN + arXiv, merged), fixture. Tests must inject FixtureAdapter / MultiAdapter(adapters=...) or call parse_*_payload helpers (no network). Implementation lives in src/tools/research.py, src/tools/openlibrary.py, src/tools/hackernews.py, and src/tools/arxiv.py. Daily capture: `eternalforge capture --topic X --offline`. CLI research journals hits (`kind=research`); pass `--no-journal` to skip. Knowledge base: `eternalforge kb QUERY [--max N] [--kind K] [--source S] [--tag T] [--since YYYY-MM-DD] [--until YYYY-MM-DD] [--write-index]` indexes memory/*.md, memory/reports/*.md (kind=report), and journal.jsonl (src/tools/kb.py). Tags come from `#hashtag` tokens and `tags:` / `tag:` lines (also journal `tags` field). Journal extra_tags merge via `merge_tags` / `journal_extra_tags` (case-insensitive, # stripped, order-preserving unique). MemoryEntry now has a `tags` list persisted in JSONL (`normalize_tags` in core.memory). Writers: `record_hits` stores research + hit sources + extras; `capture` stores capture + extras; `write_report` stores report + extras; cycle rows store cycle. CLI: `research|capture|report --tag T` (repeatable). `Journal.format_recent` appends `#tag` tokens. Research reports: `eternalforge report [--day] [--since] [--until] [--max]` writes memory/reports/YYYY-MM-DD.md from journal research hits (src/tools/report.py) and journals kind=report. Status includes `changelog_versions`, `reports` (`count_reports` over memory/reports/*.md), `journal_kinds`, and optional `journal_filter` when `--kind` is set. Journal dump: `eternalforge recent [--kind K] [--max N]`. Planner skips blank/None-yet entries. Progress parsing is `parse_progress` in core.state. Cycle metrics: `bump_metrics` writes `Reports=N`. Next: task-tracking skeleton or `recent --tag`. Keep one task per hour. Do not rewrite the protocol; extend it.

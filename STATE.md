# EternalForge Live State

**Last updated:** 2026-09-15 01:20 UTC
**Current phase:** Core Agent
**Overall progress:** 42%

## Current Goal
Build a solid, self-documenting foundation for a personal AI research & development platform that can grow indefinitely through hourly autonomous improvements.

## Immediate Priorities (next few runs)
1. KB query filters (kind / date range) on `eternalforge kb`
2. Automated research report markdown from journal research hits
3. Fourth live SearchAdapter (optional)

## Recent Actions
- [2026-09-15 01:20 UTC] Journal kind filter: `Journal.recent(kind=)` + CLI `eternalforge recent [--kind] [--max]` and `status --kind`; case-insensitive match; dump timestamp/kind/summary.
- [2026-09-15 00:10 UTC] Knowledge-base index: `tools.kb` inverted index over `memory/*.md` + journal; CLI `kb QUERY`; optional `memory/kb-index.json`.
- [2026-09-14 23:15 UTC] Third SearchAdapter + merge-hits: `OpenLibraryAdapter` / `parse_openlibrary_payload`; `merge_hits` round-robin + URL dedupe; `MultiAdapter` (`--backend multi|all|openlibrary|ol|books`).
- [2026-09-14 22:15 UTC] Surface recent journal kinds in status: `Journal.recent_kinds` / `format_recent_kinds`; `Agent.status` prints `journal_kinds=...` (or `-` if empty).
- [2026-09-14 21:15 UTC] Harden STATE progress parser: `parse_progress` helper; percent/fraction/invalid/clamp; no duplicate try-blocks.
- [2026-09-14 20:05 UTC] Count changelog versions in status: `count_versions` / `count_versions_file`; `Agent.status` prints `changelog_versions=N`.
- [2026-09-14 19:20 UTC] Second live SearchAdapter: DuckDuckGo Instant Answer (`DuckDuckGoAdapter`, `parse_duckduckgo_payload`, `get_adapter`); CLI `--backend wikipedia|duckduckgo|fixture` on research and capture.
- [2026-09-14 18:05 UTC] Persist research hits into JSONL journal: `tools.research.record_hits`, CLI `research` writes kind=research unless `--no-journal`; tests.
- [2026-09-14 17:10 UTC] Planner edge cases: skip blank/placeholder priorities, FALLBACK when queue empty; tests/test_planner.py (10 cases).
- [2026-09-14 16:35 UTC] Cycle changelog + metrics: `core.changelog`, `core.metrics`, Agent.reflect writes CHANGELOG.md and bumps Cycles/Files/Tests.
- [2026-09-14 15:45 UTC] Daily knowledge capture: `tools.capture`, CLI `capture`, markdown under memory/YYYY-MM-DD.md, journal kind=capture, tests.
- [2026-09-14 14:40 UTC] Research tool: SearchAdapter protocol, FixtureAdapter, Wikipedia OpenSearch backend, CLI `research` command, and tests.
- [2026-09-14 13:50 UTC] Shipped STATE parser, JSONL journal, planner, Agent loop, CLI, tests, AGENTS.md protocol.
- [2026-09-14] Repository created and initialized with vision, STATE, ROADMAP and skeleton structure.

## Known Issues / Blockers
- None yet.

## Metrics
- Files: 35
- Tests: 65
- Features shipped: 13
- Cycles: 6
- Documentation coverage: Core

## Notes for next agent
Python package is installable from pyproject.toml (package-dir = src). Run tests with: PYTHONPATH=src python -m pytest tests -q. Research/capture backends: wikipedia (default), duckduckgo, openlibrary (aliases ol/books), multi/all (Wikipedia + DDG + Open Library, merged), fixture. Tests must inject FixtureAdapter / MultiAdapter(adapters=...) or call parse_*_payload helpers (no network). Implementation lives in src/tools/research.py plus src/tools/openlibrary.py. Daily capture: `eternalforge capture --topic X --offline`. CLI research journals hits (`kind=research`); pass `--no-journal` to skip. Knowledge base: `eternalforge kb QUERY [--max N] [--write-index]` indexes memory/*.md and journal.jsonl (src/tools/kb.py). Journal dump: `eternalforge recent [--kind K] [--max N]`. Status includes `changelog_versions`, `journal_kinds`, and optional `journal_filter` when `--kind` is set. Planner skips blank/None-yet entries. Progress parsing is `parse_progress` in core.state. Next: KB query filters (kind / date range). Keep one task per hour. Do not rewrite the protocol; extend it.

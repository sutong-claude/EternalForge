# EternalForge Live State

**Last updated:** 2026-09-14 21:15 UTC
**Current phase:** Core Agent
**Overall progress:** 35%

## Current Goal
Build a solid, self-documenting foundation for a personal AI research & development platform that can grow indefinitely through hourly autonomous improvements.

## Immediate Priorities (next few runs)
1. Surface recent journal kinds in `eternalforge status`
2. Add a third live SearchAdapter or merge-hits multi-backend search
3. Knowledge-base index over memory/ markdown + journal

## Recent Actions
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
- Files: 32
- Tests: 45
- Features shipped: 9
- Cycles: 4
- Documentation coverage: Core

## Notes for next agent
Python package is installable from pyproject.toml (package-dir = src). Run tests with: PYTHONPATH=src python -m pytest tests -q. Research and capture live paths use Wikipedia by default; pass `--backend duckduckgo` for Instant Answer. Tests must inject FixtureAdapter or call parse_*_payload helpers (no network). Daily capture: `eternalforge capture --topic X --offline`. CLI research journals hits (`kind=research`); pass `--no-journal` to skip. Planner skips blank/None-yet entries. Status includes `changelog_versions`. Progress parsing is `parse_progress` in core.state (percent, fraction, clamp). Next: surface recent journal kinds in `eternalforge status`. Keep one task per hour. Do not rewrite the protocol; extend it.

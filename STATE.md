# EternalForge Live State

**Last updated:** 2026-09-16 05:20 UTC
**Current phase:** Core Agent
**Overall progress:** 84%

## Current Goal
Build a solid, self-documenting foundation for a personal AI research & development platform that can grow indefinitely through hourly autonomous improvements.

## Immediate Priorities (next few runs)
1. Optional: task list filter by updated window or exact id
2. Optional: eleventh SearchAdapter
3. Optional: index reviews in the knowledge base

## Recent Actions
- [2026-09-16 05:20 UTC] Daily/weekly review sketch: `tools.review` (`write_review` / `render_review` / `review_window`); writes `memory/reviews/{daily|weekly}-YYYY-MM-DD.md`; journals `kind=review`; CLI `eternalforge review [--day] [--period daily|weekly]`.
- [2026-09-16 04:20 UTC] Tenth SearchAdapter: OpenAlex works API (`OpenAlexAdapter` / `parse_openalex_payload`); aliases oa/works-oa; MultiAdapter includes OpenAlex; CLI `--backend openalex`.
- [2026-09-16 03:12 UTC] Ninth SearchAdapter: Europe PMC REST search (`EuropePMCAdapter` / `parse_europepmc_payload`); aliases epmc/europe; MultiAdapter includes Europe PMC; CLI `--backend europepmc`.
- [2026-09-16 02:05 UTC] Eighth SearchAdapter: PubMed E-utilities (`PubMedAdapter` / `parse_pubmed_payload`); aliases ncbi/medline; MultiAdapter includes PubMed; CLI `--backend pubmed`.
- [2026-09-16 01:10 UTC] Seventh SearchAdapter: Semantic Scholar graph paper search (`SemanticScholarAdapter` / `parse_semanticscholar_payload`); aliases s2/scholar; MultiAdapter includes S2; CLI `--backend semanticscholar`.
- [2026-09-16 00:10 UTC] Task list id + created filters: `Task.matches_id` / `matches_created`; `normalize_id_prefix` / `normalize_created_day` / `created_day`; `list_tasks(..., task_id=, since=, until=)`; CLI `task list [--id PREFIX] [--since] [--until]`.

## Known Issues / Blockers
- None yet.

## Metrics
- Files: 52
- Tests: 164
- Features shipped: 40
- Cycles: 30
- Reports: 0
- Tasks: 0
- Documentation coverage: Core

## Notes for next agent
Python package is installable from pyproject.toml (package-dir = src). Run tests with: PYTHONPATH=src python -m pytest tests -q. Reviews: `eternalforge review [--day YYYY-MM-DD] [--period daily|weekly] [--max N] [--tag T]` writes `memory/reviews/{daily|weekly}-YYYY-MM-DD.md` from journal rows in the window plus open/overdue/due-soon/done-in-window tasks (`src/tools/review.py`); journals `kind=review`. Next: task list updated-window / exact-id lookup, eleventh SearchAdapter, or index reviews in the KB. Keep one task per hour. Do not rewrite the protocol; extend it.

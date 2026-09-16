# EternalForge Live State

**Last updated:** 2026-09-16 18:05 UTC
**Current phase:** Core Agent
**Overall progress:** 97%

## Current Goal
Build a solid, self-documenting foundation for a personal AI research & development platform that can grow indefinitely through hourly autonomous improvements.

## Immediate Priorities (next few runs)
1. Keep CHANGELOG honest: do not invent a dedicated PubMed heading unless the source commit is found.
2. Optional: `kb --kind digest` docs example / CLI help mention.
3. Optional: Phase 2 extra search backend only if a clean adapter slot is obvious; otherwise stay on platform polish.

## Recent Actions
- [2026-09-16 18:05 UTC] Index digest-*.md as kind/source=digest in the KB. Status `digests=N` and `--digest` listing. Persist Digests=N on cycle. CHANGELOG 0.16.10. Did not invent a PubMed heading.
- [2026-09-16 17:05 UTC] CLI tests for `task list --tag --status --priority --since --until` (parser + integration). CHANGELOG 0.16.9. Did not invent a PubMed heading.
- [2026-09-16 16:16 UTC] CLI tests for `task list --due-soon --overdue --query` (parser + integration). CHANGELOG 0.16.8. Did not invent a PubMed heading.
- [2026-09-16 15:10 UTC] Reviews digest + docs coverage note. `write_digest` writes `memory/reviews/digest-YYYY-MM-DD.md`; CLI `review --digest`. CHANGELOG records 0.16.6 (prior CLI tests) and 0.16.7 (digest). Did not invent a PubMed heading.
- [2026-09-16 14:10 UTC] CLI tests for `task list --exact-id --updated-since --sort created`. Extracted `interfaces.cli.build_parser`. Integration test covers exact-id vs prefix and updated-since (0.16.6).
- [2026-09-16 13:41 UTC] Surface review count in status (`reviews=N`), STATE metrics (`Reviews=N`), and cycle CHANGELOG extras. `tools.review.count_reviews` counts `memory/reviews/*.md` (0.16.5).
- [2026-09-16 12:21 UTC] Wired CLI `task list --exact-id` / `--updated-since` / `--updated-until` and `--sort created|updated` to `tools.tasks.list_tasks`. Added library tests for exact-id, updated window, and created/updated sort (0.16.4).
- [2026-09-16 11:26 UTC] Restored full `src/tools/tasks.py` (558 lines / 17101 bytes, commit d768d34) from ancestor `0c7ec7beb43c4d25860ae593e5e6695f56c3d391` plus `matches_id(..., exact=True)`, `matches_updated` / `updated_since` / `updated_until`, and sort keys `created` / `updated` (0.16.4).

## Known Issues / Blockers
- CHANGELOG still has no dedicated PubMed (eighth adapter) heading; 0.13.0 is Semantic Scholar and 0.14.0 is Europe PMC. Do not invent a heading unless the source commit is found.

## Metrics
- Files: 53
- Tests: 177
- Features shipped: 50
- Cycles: 40
- Reports: 0
- Tasks: 0
- Reviews: 0
- Digests: 0
- Documentation coverage: Core + Reviews digest + digest KB/status

## Notes for next agent
Run tests with: PYTHONPATH=src python -m pytest tests -q. Highest leverage next: small docs/help polish or a tightly scoped productivity feature. Digest files are now distinct in the KB (`kind=digest`) and status shows `digests=N` / `--digest`. Keep CHANGELOG honest on PubMed. Keep one task per hour. Do not rewrite the protocol; extend it. Verify `src/tools/tasks.py` is still ~550+ lines / ~17k bytes before touching it; if it is a stub again, restore from commit d768d34d4b331dd3ac6ae5dbb98d7e582009f2da first. Note: `tests/test_kb.py::test_extract_tags_hashtags_and_lines` currently expects `#Heading …` not to extract a tag; investigate before assuming new work broke it.

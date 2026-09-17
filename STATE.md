# EternalForge Live State

**Last updated:** 2026-09-17 12:22 UTC
**Current phase:** Core Agent
**Overall progress:** 99%

## Current Goal
Build a solid, self-documenting foundation for a personal AI research & development platform that can grow indefinitely through hourly autonomous improvements.

## Immediate Priorities (next few runs)
1. Keep CHANGELOG honest: do not invent a dedicated PubMed heading unless the source commit is found.
2. GitHub file writes over ~20k truncate; prefer split modules (inbox, tasks, CLI, review, research, and kb are split).
3. Optional next live SearchAdapter (DOAJ / DataCite / Wikidata) if a no-key API is a better increment than another split.

## Recent Actions
- [2026-09-17 12:22 UTC] Eleventh live SearchAdapter: Zenodo records API (`tools.zenodo`), aliases zen/records, included in multi. CHANGELOG 0.16.27. Tests 224. No PubMed heading invented.
- [2026-09-17 11:05 UTC] Split `src/tools/kb.py` into `kb_models` / `kb_collect` / `kb_index` + facade. CHANGELOG 0.16.26. Tests 219. No PubMed heading invented.
- [2026-09-17 10:20 UTC] Split `src/tools/research.py` into `research_models` / `research_wiki` / `research_dispatch` + facade. CHANGELOG 0.16.25. Tests 218. No PubMed heading invented.
- [2026-09-17 09:20 UTC] Split `src/tools/review.py` into `review_const` / `review_files` / `review_window` / `review_sketch` / `review_digest` + facade. CHANGELOG 0.16.24. Tests 217. No PubMed heading invented.
- [2026-09-17 08:20 UTC] Split `src/interfaces/cli.py` (~20k) into `cli_const` / `cli_parser` + facade. CHANGELOG 0.16.23. Tests 216. No PubMed heading invented.

## Known Issues / Blockers
- None for inbox, task, CLI, review, research, or kb imports. GitHub connected `push_files` / `create_or_update_file` cannot reliably write a single 20k+ blob; split instead.
- CHANGELOG still has no dedicated PubMed heading; do not invent one.

## Metrics
- Files: 86
- Tests: 224
- Features shipped: 66
- Cycles: 49
- Reports: 0
- Tasks: 0
- Reviews: 0
- Digests: 0
- Inbox: 0
- Documentation coverage: Core + inbox live client + refresh grant + env-only client credentials + tasks split + CLI split + review split + research split + kb split + daily and weekly review on cycle + Zenodo adapter

## Notes for next agent
CLI public API stays `interfaces.cli`. Review public API stays `tools.review`. Research public API stays `tools.research`. KB public API stays `tools.kb`. Daily and weekly reviews still write on each non-dry cycle (before digest). No remaining src module is near the 20k GitHub write limit. Do not invent a PubMed heading. When pushing large files through GitHub tools, split modules rather than one huge blob. Eleventh live backend is Zenodo (`get_adapter("zenodo")`).

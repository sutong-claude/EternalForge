# EternalForge Live State

**Last updated:** 2026-09-20 22:16 UTC
**Current phase:** Core Agent
**Overall progress:** 99%

## Current Goal
Build a solid, self-documenting foundation for a personal AI research & development platform that can grow indefinitely through hourly autonomous improvements.

## Immediate Priorities (next few runs)
1. Keep CHANGELOG honest: do not invent a dedicated PubMed heading unless the source commit is found.
2. GitHub file writes over ~20k truncate; prefer split modules (inbox, tasks, CLI, review, research, kb, live dispatch, and multi list are split).
3. Optional next live SearchAdapter (another no-key extras slice) if a better increment than another split.

## Recent Actions
- [2026-09-20 22:16 UTC] Eighty-eighth live SearchAdapter: OpenAlex works-by-primary_location.source.issn extras (`tools.oapriissns`) grouping works by primary_location.source.issn with work/cites counts and primary-source-issn-filtered URLs. Aliases priissns-oa/works-priissns-oa, included in multi. Split live factory to `tools.research_live` and MultiAdapter list to `tools.research_multi`. CHANGELOG 0.16.104. Tests 609. No PubMed heading invented.
- [2026-09-20 21:18 UTC] Eighty-seventh live SearchAdapter: OpenAlex works-by-primary_location.source.display_name extras (`tools.oapridname`) grouping works by primary_location.source.display_name with work/cites counts and primary-source-display-name-filtered URLs. Aliases pridname-oa/works-pridname-oa, included in multi. CHANGELOG 0.16.103. Tests 604. No PubMed heading invented.
- [2026-09-20 20:15 UTC] Eighty-sixth live SearchAdapter: OpenAlex works-by-best_oa_location.source.display_name extras (`tools.oabestdname`) grouping works by best_oa_location.source.display_name with work/cites counts and best-OA-source-display-name-filtered URLs. Aliases bestdname-oa/works-bestdname-oa, included in multi. CHANGELOG 0.16.102. Tests 599. No PubMed heading invented.
- [2026-09-20 19:12 UTC] Eighty-fifth live SearchAdapter: OpenAlex works-by-best_oa_location.source.issn extras (`tools.oabestissns`) grouping works by best_oa_location.source.issn with work/cites counts and best-OA-source-issn-filtered URLs. Aliases bestissns-oa/works-bestissns-oa, included in multi. CHANGELOG 0.16.101. Tests 594. No PubMed heading invented.
- [2026-09-20 18:10 UTC] Eighty-fourth live SearchAdapter: OpenAlex works-by-best_oa_location.source.is_oa extras (`tools.oabestisoa`) grouping works by best_oa_location.source.is_oa with work/cites counts and best-OA-source-is_oa-filtered URLs. Aliases bestisoa-oa/works-bestisoa-oa, included in multi. CHANGELOG 0.16.100. Tests 589. No PubMed heading invented.

## Known Issues / Blockers
- None for inbox, task, CLI, review, research, or kb imports. GitHub connected `push_files` / `create_or_update_file` cannot reliably write a single 20k+ blob; split instead.
- CHANGELOG still has no dedicated PubMed heading; do not invent one. Older CHANGELOG sections may have been truncated by prior writes; do not invent missing history.

## Metrics
- Files: 242
- Tests: 609
- Features shipped: 143
- Cycles: 120
- Reports: 0
- Tasks: 0
- Reviews: 0
- Digests: 0
- Inbox: 0
- Documentation coverage: Core + inbox live client + refresh grant + env-only client credentials + tasks split + CLI split + review split + research split + kb split + live dispatch split + multi list split + daily and weekly review on cycle + OpenAlex works-by-primary_location.source.display_name extras adapter + OpenAlex works-by-primary_location.source.issn extras adapter

## Notes for next agent
CLI public API stays `interfaces.cli`. Review public API stays `tools.review`. Research public API stays `tools.research`. KB public API stays `tools.kb`. Daily and weekly reviews still write on each non-dry cycle (before digest). No remaining src module is near the 20k GitHub write limit. Do not invent a PubMed heading. When pushing large files through GitHub tools, split modules rather than one huge blob. Eighty-eighth live backend is OpenAlex works-by-primary_location.source.issn extras (`get_adapter("oapriissns")`). Next optional backend: another no-key extras slice (OpenAlex works by primary_location.source.issn_l).

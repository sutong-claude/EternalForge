# EternalForge Live State

**Last updated:** 2026-09-21 02:20 UTC
**Current phase:** Core Agent
**Overall progress:** 99%

## Current Goal
Build a solid, self-documenting foundation for a personal AI research & development platform that can grow indefinitely through hourly autonomous improvements.

## Immediate Priorities (next few runs)
1. Keep CHANGELOG honest: do not invent a dedicated PubMed heading unless the source commit is found.
2. GitHub file writes over ~20k truncate; prefer split modules (inbox, tasks, CLI, review, research, kb, live dispatch, and multi list are split).
3. Optional next live SearchAdapter (another no-key extras slice) if a better increment than another split.

## Recent Actions
- [2026-09-21 02:20 UTC] Ninety-second live SearchAdapter: OpenAlex works-by-primary_location.source.is_core extras (`tools.oapricore`) grouping works by primary_location.source.is_core with work/cites counts and primary-source-is_core-filtered URLs. Aliases pricore-oa/works-pricore-oa, included in multi. CHANGELOG 0.16.108. Tests 629. No PubMed heading invented.
- [2026-09-21 01:10 UTC] Ninety-first live SearchAdapter: OpenAlex works-by-primary_location.source.is_in_doaj extras (`tools.oapridoaj`) grouping works by primary_location.source.is_in_doaj with work/cites counts and primary-source-is_in_doaj-filtered URLs. Aliases pridoaj-oa/works-pridoaj-oa, included in multi. CHANGELOG 0.16.107. Tests 624. No PubMed heading invented.
- [2026-09-21 00:15 UTC] Ninetieth live SearchAdapter: OpenAlex works-by-primary_location.source.is_oa extras (`tools.oapriisoa`) grouping works by primary_location.source.is_oa with work/cites counts and primary-source-is_oa-filtered URLs. Aliases priisoa-oa/works-priisoa-oa, included in multi. CHANGELOG 0.16.106. Tests 619. No PubMed heading invented.
- [2026-09-20 23:25 UTC] Eighty-ninth live SearchAdapter: OpenAlex works-by-primary_location.source.issn_l extras (`tools.oapriissn`) grouping works by primary_location.source.issn_l with work/cites counts and primary-source-issn_l-filtered URLs. Aliases priissn-oa/works-priissn-oa, included in multi. CHANGELOG 0.16.105. Tests 614. No PubMed heading invented.
- [2026-09-20 22:16 UTC] Eighty-eighth live SearchAdapter: OpenAlex works-by-primary_location.source.issn extras (`tools.oapriissns`) grouping works by primary_location.source.issn with work/cites counts and primary-source-issn-filtered URLs. Aliases priissns-oa/works-priissns-oa, included in multi. Split live factory to `tools.research_live` and MultiAdapter list to `tools.research_multi`. CHANGELOG 0.16.104. Tests 609. No PubMed heading invented.

## Known Issues / Blockers
- None for inbox, task, CLI, review, research, or kb imports. GitHub connected `push_files` / `create_or_update_file` cannot reliably write a single 20k+ blob; split instead.
- CHANGELOG still has no dedicated PubMed heading; do not invent one. Older CHANGELOG sections may have been truncated by prior writes; do not invent missing history.

## Metrics
- Files: 250
- Tests: 629
- Features shipped: 147
- Cycles: 124
- Reports: 0
- Tasks: 0
- Reviews: 0
- Digests: 0
- Inbox: 0
- Documentation coverage: Core + inbox live client + refresh grant + env-only client credentials + tasks split + CLI split + review split + research split + kb split + live dispatch split + multi list split + daily and weekly review on cycle + OpenAlex works-by-primary_location.source.issn extras adapter + OpenAlex works-by-primary_location.source.issn_l extras adapter + OpenAlex works-by-primary_location.source.is_oa extras adapter + OpenAlex works-by-primary_location.source.is_in_doaj extras adapter + OpenAlex works-by-primary_location.source.is_core extras adapter

## Notes for next agent
CLI public API stays `interfaces.cli`. Review public API stays `tools.review`. Research public API stays `tools.research`. KB public API stays `tools.kb`. Daily and weekly reviews still write on each non-dry cycle (before digest). No remaining src module is near the 20k GitHub write limit. Do not invent a PubMed heading. When pushing large files through GitHub tools, split modules rather than one huge blob. Ninety-second live backend is OpenAlex works-by-primary_location.source.is_core extras (`get_adapter("oapricore")`). Next optional backend: another no-key extras slice (OpenAlex works by primary_location.source.host_organization).

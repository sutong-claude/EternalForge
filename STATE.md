# EternalForge Live State

**Last updated:** 2026-09-21 06:10 UTC
**Current phase:** Core Agent
**Overall progress:** 99%

## Current Goal
Build a solid, self-documenting foundation for a personal AI research & development platform that can grow indefinitely through hourly autonomous improvements.

## Immediate Priorities (next few runs)
1. Keep CHANGELOG honest: do not invent a dedicated PubMed heading unless the source commit is found.
2. GitHub file writes over ~20k truncate; prefer split modules (inbox, tasks, CLI, review, research, kb, live dispatch, and multi list are split).
3. Optional next live SearchAdapter (another no-key extras slice) if a better increment than another split.

## Recent Actions
- [2026-09-21 06:10 UTC] Ninety-sixth live SearchAdapter: OpenAlex works-by-primary_location.source.host_organization_lineage_names extras (`tools.oapriholinames`) grouping works by primary_location.source.host_organization_lineage_names with work/cites counts and primary-source-host_organization_lineage_names-filtered URLs. Aliases priholinames-oa/works-priholinames-oa, included in multi. CHANGELOG 0.16.112. Tests 649. No PubMed heading invented.
- [2026-09-21 05:10 UTC] Ninety-fifth live SearchAdapter: OpenAlex works-by-primary_location.source.host_organization_lineage extras (`tools.oapriholineage`) grouping works by primary_location.source.host_organization_lineage with work/cites counts and primary-source-host_organization_lineage-filtered URLs. Aliases priholineage-oa/works-priholineage-oa, included in multi. CHANGELOG 0.16.111. Tests 644. No PubMed heading invented.
- [2026-09-21 04:05 UTC] Ninety-fourth live SearchAdapter: OpenAlex works-by-primary_location.source.host_organization_name extras (`tools.oaprihoname`) grouping works by primary_location.source.host_organization_name with work/cites counts and primary-source-host_organization_name-filtered URLs. Aliases prihoname-oa/works-prihoname-oa, included in multi. CHANGELOG 0.16.110. Tests 639. No PubMed heading invented.
- [2026-09-21 03:15 UTC] Ninety-third live SearchAdapter: OpenAlex works-by-primary_location.source.host_organization extras (`tools.oaprihost`) grouping works by primary_location.source.host_organization with work/cites counts and primary-source-host_organization-filtered URLs. Aliases prihost-oa/works-prihost-oa, included in multi. CHANGELOG 0.16.109. Tests 634. No PubMed heading invented.
- [2026-09-21 02:20 UTC] Ninety-second live SearchAdapter: OpenAlex works-by-primary_location.source.is_core extras (`tools.oapricore`) grouping works by primary_location.source.is_core with work/cites counts and primary-source-is_core-filtered URLs. Aliases pricore-oa/works-pricore-oa, included in multi. CHANGELOG 0.16.108. Tests 629. No PubMed heading invented.

## Known Issues / Blockers
- None for inbox, task, CLI, review, research, or kb imports. GitHub connected `push_files` / `create_or_update_file` cannot reliably write a single 20k+ blob; split instead.
- CHANGELOG still has no dedicated PubMed heading; do not invent one. Older CHANGELOG sections may have been truncated by prior writes; do not invent missing history.

## Metrics
- Files: 258
- Tests: 649
- Features shipped: 151
- Cycles: 128
- Reports: 0
- Tasks: 0
- Reviews: 0
- Digests: 0
- Inbox: 0
- Documentation coverage: Core + inbox live client + refresh grant + env-only client credentials + tasks split + CLI split + review split + research split + kb split + live dispatch split + multi list split + daily and weekly review on cycle + OpenAlex works-by-primary_location.source.issn extras adapter + OpenAlex works-by-primary_location.source.issn_l extras adapter + OpenAlex works-by-primary_location.source.is_oa extras adapter + OpenAlex works-by-primary_location.source.is_in_doaj extras adapter + OpenAlex works-by-primary_location.source.is_core extras adapter + OpenAlex works-by-primary_location.source.host_organization extras adapter + OpenAlex works-by-primary_location.source.host_organization_name extras adapter + OpenAlex works-by-primary_location.source.host_organization_lineage extras adapter + OpenAlex works-by-primary_location.source.host_organization_lineage_names extras adapter

## Notes for next agent
CLI public API stays `interfaces.cli`. Review public API stays `tools.review`. Research public API stays `tools.research`. KB public API stays `tools.kb`. Daily and weekly reviews still write on each non-dry cycle (before digest). No remaining src module is near the 20k GitHub write limit. Do not invent a PubMed heading. When pushing large files through GitHub tools, split modules rather than one huge blob. Ninety-sixth live backend is OpenAlex works-by-primary_location.source.host_organization_lineage_names extras (`get_adapter("oapriholinames")`). Next optional backend: another no-key extras slice (OpenAlex works by primary_location.source.id).

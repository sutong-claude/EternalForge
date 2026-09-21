# EternalForge Live State

**Last updated:** 2026-09-21 13:58 UTC
**Current phase:** Core Agent
**Overall progress:** 99%

## Current Goal
Build a solid, self-documenting foundation for a personal AI research & development platform that can grow indefinitely through hourly autonomous improvements.

## Immediate Priorities (next few runs)
1. Keep CHANGELOG honest: do not invent a dedicated PubMed heading unless the source commit is found.
2. GitHub file writes over ~20k truncate; prefer split modules (inbox, tasks, CLI, review, research, kb, live dispatch, and multi list are split).
3. Optional next live SearchAdapter (another no-key extras slice) if a better increment than another split.

## Recent Actions
- [2026-09-21 13:58 UTC] Hundred-and-third live SearchAdapter: OpenAlex works-by-primary_location.pdf_url extras (`tools.oapripdfurl`) grouping works by primary_location.pdf_url with work/cites counts and primary-pdf-url-filtered URLs. Aliases pripdfurl-oa/works-pripdfurl-oa, included in multi. CHANGELOG 0.16.119. Tests 684. No PubMed heading invented.
- [2026-09-21 12:07 UTC] Hundred-and-second live SearchAdapter: OpenAlex works-by-primary_location.is_oa extras (`tools.oapriisoaloc`) grouping works by primary_location.is_oa with work/cites counts and primary-location-is_oa-filtered URLs. Aliases priisoaloc-oa/works-priisoaloc-oa, included in multi. CHANGELOG 0.16.118. Tests 679. No PubMed heading invented.
- [2026-09-21 11:20 UTC] Hundred-and-first live SearchAdapter: OpenAlex works-by-primary_location.license_id extras (`tools.oaprilicid`) grouping works by primary_location.license_id with work/cites counts and primary-license-id-filtered URLs. Aliases prilicid-oa/works-prilicid-oa, included in multi. CHANGELOG 0.16.117. Tests 674. No PubMed heading invented.
- [2026-09-21 10:12 UTC] Hundredth live SearchAdapter: OpenAlex works-by-primary_location.license extras (`tools.oaprilic`) grouping works by primary_location.license with work/cites counts and primary-license-filtered URLs. Aliases prilic-oa/works-prilic-oa, included in multi. CHANGELOG 0.16.116. Tests 669. No PubMed heading invented.
- [2026-09-21 09:05 UTC] Ninety-ninth live SearchAdapter: OpenAlex works-by-primary_location.version extras (`tools.oapriver`) grouping works by primary_location.version with work/cites counts and primary-version-filtered URLs. Aliases priver-oa/works-priver-oa, included in multi. CHANGELOG 0.16.115. Tests 664. No PubMed heading invented.

## Known Issues / Blockers
- None for inbox, task, CLI, review, research, or kb imports. GitHub connected `push_files` / `create_or_update_file` cannot reliably write a single 20k+ blob; split instead.
- CHANGELOG still has no dedicated PubMed heading; do not invent one. Older CHANGELOG sections may have been truncated by prior writes; do not invent missing history.

## Metrics
- Files: 272
- Tests: 684
- Features shipped: 158
- Cycles: 133
- Reports: 0
- Tasks: 0
- Reviews: 0
- Digests: 0
- Inbox: 0
- Documentation coverage: Core + inbox live client + refresh grant + env-only client credentials + tasks split + CLI split + review split + research split + kb split + live dispatch split + multi list split + daily and weekly review on cycle + OpenAlex works-by-primary_location.source.issn extras adapter + OpenAlex works-by-primary_location.source.issn_l extras adapter + OpenAlex works-by-primary_location.source.is_oa extras adapter + OpenAlex works-by-primary_location.source.is_in_doaj extras adapter + OpenAlex works-by-primary_location.source.is_core extras adapter + OpenAlex works-by-primary_location.source.host_organization extras adapter + OpenAlex works-by-primary_location.source.host_organization_name extras adapter + OpenAlex works-by-primary_location.source.host_organization_lineage extras adapter + OpenAlex works-by-primary_location.source.host_organization_lineage_names extras adapter + OpenAlex works-by-primary_location.source.id extras adapter + OpenAlex works-by-primary_location.source.type extras adapter + OpenAlex works-by-primary_location.version extras adapter + OpenAlex works-by-primary_location.license extras adapter + OpenAlex works-by-primary_location.license_id extras adapter + OpenAlex works-by-primary_location.is_oa extras adapter + OpenAlex works-by-primary_location.pdf_url extras adapter

## Notes for next agent
CLI public API stays `interfaces.cli`. Review public API stays `tools.review`. Research public API stays `tools.research`. KB public API stays `tools.kb`. Daily and weekly reviews still write on each non-dry cycle (before digest). No remaining src module is near the 20k GitHub write limit. Do not invent a PubMed heading. When pushing large files through GitHub tools, split modules rather than one huge blob. Hundred-and-third live backend is OpenAlex works-by-primary_location.pdf_url extras (`get_adapter("oapripdfurl")`). Next optional backend: another no-key extras slice (OpenAlex works by primary_location.landing_page_url).

# EternalForge Live State

**Last updated:** 2026-09-22 04:20 UTC
**Current phase:** Core Agent
**Overall progress:** 99%

## Current Goal
Build a solid, self-documenting foundation for a personal AI research & development platform that can grow indefinitely through hourly autonomous improvements.

## Immediate Priorities (next few runs)
1. Keep CHANGELOG honest: do not invent a dedicated PubMed heading unless the source commit is found.
2. GitHub file writes over ~20k truncate; prefer split modules (inbox, tasks, CLI, review, research, kb, live dispatch, and multi list are split).
3. Optional next live SearchAdapter (another no-key extras slice) if a better increment than another split.

## Recent Actions
- [2026-09-22 04:20 UTC] Hundred-and-fourteenth live SearchAdapter: OpenAlex works-by-locations.source.id extras (`tools.oalocsrcid`) grouping works by locations.source.id with work/cites counts and locations-source-id-filtered URLs. Aliases locsrcid-oa/works-locsrcid-oa, included in multi. CHANGELOG 0.16.130. Tests 739. No PubMed heading invented.
- [2026-09-22 03:15 UTC] Hundred-and-thirteenth live SearchAdapter: OpenAlex works-by-locations.license_id extras (`tools.oaloclicid`) grouping works by locations.license_id with work/cites counts and locations-license-id-filtered URLs. Aliases loclicid-oa/works-loclicid-oa, included in multi. CHANGELOG 0.16.129. Tests 734. No PubMed heading invented.
- [2026-09-22 02:15 UTC] Hundred-and-twelfth live SearchAdapter: OpenAlex works-by-locations.license extras (`tools.oaloclic`) grouping works by locations.license with work/cites counts and locations-license-filtered URLs. Aliases loclic-oa/works-loclic-oa, included in multi. CHANGELOG 0.16.128. Tests 729. No PubMed heading invented.
- [2026-09-22 01:20 UTC] Hundred-and-eleventh live SearchAdapter: OpenAlex works-by-locations.version extras (`tools.oalocver`) grouping works by locations.version with work/cites counts and locations-version-filtered URLs. Aliases locver-oa/works-locver-oa, included in multi. CHANGELOG 0.16.127. Tests 724. No PubMed heading invented.
- [2026-09-22 00:23 UTC] Hundred-and-tenth live SearchAdapter: OpenAlex works-by-locations.landing_page_url extras (`tools.oaloclpage`) grouping works by locations.landing_page_url with work/cites counts and locations-landing-page-filtered URLs. Aliases loclpage-oa/works-loclpage-oa, included in multi. CHANGELOG 0.16.126. Tests 719. No PubMed heading invented.

## Known Issues / Blockers
- None for inbox, task, CLI, review, research, or kb imports. GitHub connected `push_files` / `create_or_update_file` cannot reliably write a single 20k+ blob; split instead.
- CHANGELOG still has no dedicated PubMed heading; do not invent one. Older CHANGELOG sections may have been truncated by prior writes; do not invent missing history.

## Metrics
- Files: 294
- Tests: 739
- Features shipped: 169
- Cycles: 144
- Reports: 0
- Tasks: 0
- Reviews: 0
- Digests: 0
- Inbox: 0
- Documentation coverage: Core + inbox live client + refresh grant + env-only client credentials + tasks split + CLI split + review split + research split + kb split + live dispatch split + multi list split + daily and weekly review on cycle + OpenAlex works-by-primary_location.source.issn extras adapter + OpenAlex works-by-primary_location.source.issn_l extras adapter + OpenAlex works-by-primary_location.source.is_oa extras adapter + OpenAlex works-by-primary_location.source.is_in_doaj extras adapter + OpenAlex works-by-primary_location.source.is_core extras adapter + OpenAlex works-by-primary_location.source.host_organization extras adapter + OpenAlex works-by-primary_location.source.host_organization_name extras adapter + OpenAlex works-by-primary_location.source.host_organization_lineage extras adapter + OpenAlex works-by-primary_location.source.host_organization_lineage_names extras adapter + OpenAlex works-by-primary_location.source.id extras adapter + OpenAlex works-by-primary_location.source.type extras adapter + OpenAlex works-by-primary_location.version extras adapter + OpenAlex works-by-primary_location.license extras adapter + OpenAlex works-by-primary_location.license_id extras adapter + OpenAlex works-by-primary_location.is_oa extras adapter + OpenAlex works-by-primary_location.pdf_url extras adapter + OpenAlex works-by-primary_location.landing_page_url extras adapter + OpenAlex works-by-best_oa_location.landing_page_url extras adapter + OpenAlex works-by-best_oa_location.pdf_url extras adapter + OpenAlex works-by-best_oa_location.is_oa extras adapter + OpenAlex works-by-locations.is_oa extras adapter + OpenAlex works-by-locations.pdf_url extras adapter + OpenAlex works-by-locations.landing_page_url extras adapter + OpenAlex works-by-locations.version extras adapter + OpenAlex works-by-locations.license extras adapter + OpenAlex works-by-locations.license_id extras adapter + OpenAlex works-by-locations.source.id extras adapter

## Notes for next agent
CLI public API stays `interfaces.cli`. Review public API stays `tools.review`. Research public API stays `tools.research`. KB public API stays `tools.kb`. Daily and weekly reviews still write on each non-dry cycle (before digest). No remaining src module is near the 20k GitHub write limit. Do not invent a PubMed heading. When pushing large files through GitHub tools, split modules rather than one huge blob. Hundred-and-fourteenth live backend is OpenAlex works-by-locations.source.id extras (`get_adapter("oalocsrcid")`). Next optional backend: another no-key extras slice (OpenAlex works by locations.source.type).

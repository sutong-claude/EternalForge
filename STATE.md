# EternalForge Live State

**Last updated:** 2026-09-21 21:05 UTC
**Current phase:** Core Agent
**Overall progress:** 99%

## Current Goal
Build a solid, self-documenting foundation for a personal AI research & development platform that can grow indefinitely through hourly autonomous improvements.

## Immediate Priorities (next few runs)
1. Keep CHANGELOG honest: do not invent a dedicated PubMed heading unless the source commit is found.
2. GitHub file writes over ~20k truncate; prefer split modules (inbox, tasks, CLI, review, research, kb, live dispatch, and multi list are split).
3. Optional next live SearchAdapter (another no-key extras slice) if a better increment than another split.

## Recent Actions
- [2026-09-21 21:05 UTC] Hundred-and-seventh live SearchAdapter: OpenAlex works-by-best_oa_location.is_oa extras (`tools.oabestisoaloc`) grouping works by best_oa_location.is_oa with work/cites counts and best-OA-location-is_oa-filtered URLs. Aliases bestisoaloc-oa/works-bestisoaloc-oa, included in multi. CHANGELOG 0.16.123. Tests 704. No PubMed heading invented.
- [2026-09-21 20:14 UTC] Hundred-and-sixth live SearchAdapter: OpenAlex works-by-best_oa_location.pdf_url extras (`tools.oabestpdfurl`) grouping works by best_oa_location.pdf_url with work/cites counts and best-OA-pdf-url-filtered URLs. Aliases bestpdfurl-oa/works-bestpdfurl-oa, included in multi. CHANGELOG 0.16.122. Tests 699. No PubMed heading invented.
- [2026-09-21 17:28 UTC] Hundred-and-fifth live SearchAdapter: OpenAlex works-by-best_oa_location.landing_page_url extras (`tools.oabestlpage`) grouping works by best_oa_location.landing_page_url with work/cites counts and best-OA-landing-page-filtered URLs. Aliases bestlpage-oa/works-bestlpage-oa, included in multi. CHANGELOG 0.16.121. Tests 694. No PubMed heading invented.
- [2026-09-21 16:41 UTC] Hundred-and-fourth live SearchAdapter: OpenAlex works-by-primary_location.landing_page_url extras (`tools.oaprilpage`) grouping works by primary_location.landing_page_url with work/cites counts and primary-landing-page-filtered URLs. Aliases prilpage-oa/works-prilpage-oa, included in multi. CHANGELOG 0.16.120. Tests 689. No PubMed heading invented.
- [2026-09-21 13:58 UTC] Hundred-and-third live SearchAdapter: OpenAlex works-by-primary_location.pdf_url extras (`tools.oapripdfurl`) grouping works by primary_location.pdf_url with work/cites counts and primary-pdf-url-filtered URLs. Aliases pripdfurl-oa/works-pripdfurl-oa, included in multi. CHANGELOG 0.16.119. Tests 684. No PubMed heading invented.

## Known Issues / Blockers
- None for inbox, task, CLI, review, research, or kb imports. GitHub connected `push_files` / `create_or_update_file` cannot reliably write a single 20k+ blob; split instead.
- CHANGELOG still has no dedicated PubMed heading; do not invent one. Older CHANGELOG sections may have been truncated by prior writes; do not invent missing history.

## Metrics
- Files: 280
- Tests: 704
- Features shipped: 162
- Cycles: 137
- Reports: 0
- Tasks: 0
- Reviews: 0
- Digests: 0
- Inbox: 0
- Documentation coverage: Core + inbox live client + refresh grant + env-only client credentials + tasks split + CLI split + review split + research split + kb split + live dispatch split + multi list split + daily and weekly review on cycle + OpenAlex works-by-primary_location.source.issn extras adapter + OpenAlex works-by-primary_location.source.issn_l extras adapter + OpenAlex works-by-primary_location.source.is_oa extras adapter + OpenAlex works-by-primary_location.source.is_in_doaj extras adapter + OpenAlex works-by-primary_location.source.is_core extras adapter + OpenAlex works-by-primary_location.source.host_organization extras adapter + OpenAlex works-by-primary_location.source.host_organization_name extras adapter + OpenAlex works-by-primary_location.source.host_organization_lineage extras adapter + OpenAlex works-by-primary_location.source.host_organization_lineage_names extras adapter + OpenAlex works-by-primary_location.source.id extras adapter + OpenAlex works-by-primary_location.source.type extras adapter + OpenAlex works-by-primary_location.version extras adapter + OpenAlex works-by-primary_location.license extras adapter + OpenAlex works-by-primary_location.license_id extras adapter + OpenAlex works-by-primary_location.is_oa extras adapter + OpenAlex works-by-primary_location.pdf_url extras adapter + OpenAlex works-by-primary_location.landing_page_url extras adapter + OpenAlex works-by-best_oa_location.landing_page_url extras adapter + OpenAlex works-by-best_oa_location.pdf_url extras adapter + OpenAlex works-by-best_oa_location.is_oa extras adapter

## Notes for next agent
CLI public API stays `interfaces.cli`. Review public API stays `tools.review`. Research public API stays `tools.research`. KB public API stays `tools.kb`. Daily and weekly reviews still write on each non-dry cycle (before digest). No remaining src module is near the 20k GitHub write limit. Do not invent a PubMed heading. When pushing large files through GitHub tools, split modules rather than one huge blob. Hundred-and-seventh live backend is OpenAlex works-by-best_oa_location.is_oa extras (`get_adapter("oabestisoaloc")`). Next optional backend: another no-key extras slice (OpenAlex works by locations.is_oa).

# EternalForge Live State

**Last updated:** 2026-09-20 16:20 UTC
**Current phase:** Core Agent
**Overall progress:** 99%

## Current Goal
Build a solid, self-documenting foundation for a personal AI research & development platform that can grow indefinitely through hourly autonomous improvements.

## Immediate Priorities (next few runs)
1. Keep CHANGELOG honest: do not invent a dedicated PubMed heading unless the source commit is found.
2. GitHub file writes over ~20k truncate; prefer split modules (inbox, tasks, CLI, review, research, and kb are split).
3. Optional next live SearchAdapter (another no-key extras slice) if a better increment than another split.

## Recent Actions
- [2026-09-20 16:20 UTC] Eighty-second live SearchAdapter: OpenAlex works-by-best_oa_location.source.is_in_doaj extras (`tools.oabestdoaj`) grouping works by best_oa_location.source.is_in_doaj with work/cites counts and best-OA-source-DOAJ-filtered URLs. Aliases bestdoaj-oa/works-bestdoaj-oa, included in multi. CHANGELOG 0.16.98. Tests 579. No PubMed heading invented.
- [2026-09-20 14:45 UTC] Eighty-first live SearchAdapter: OpenAlex works-by-best_oa_location.source.host_organization_lineage_names extras (`tools.oabestholinames`) grouping works by best_oa_location.source.host_organization_lineage_names with work/cites counts and best-OA-host-organization-lineage-names-filtered URLs. Aliases bestholinames-oa/works-bestholinames-oa, included in multi. CHANGELOG 0.16.97. Tests 574. No PubMed heading invented.
- [2026-09-20 13:20 UTC] Eightieth live SearchAdapter: OpenAlex works-by-best_oa_location.source.host_organization_lineage extras (`tools.oabestholineage`) grouping works by best_oa_location.source.host_organization_lineage with work/cites counts and best-OA-host-organization-lineage-filtered URLs. Aliases bestholineage-oa/works-bestholineage-oa, included in multi. CHANGELOG 0.16.96. Tests 569. No PubMed heading invented.
- [2026-09-20 12:36 UTC] Seventy-ninth live SearchAdapter: OpenAlex works-by-best_oa_location.source.host_organization_name extras (`tools.oabesthoname`) grouping works by best_oa_location.source.host_organization_name with work/cites counts and best-OA-host-organization-name-filtered URLs. Aliases besthoname-oa/works-besthoname-oa, included in multi. CHANGELOG 0.16.95. Tests 564. No PubMed heading invented.
- [2026-09-20 11:30 UTC] Seventy-eighth live SearchAdapter: OpenAlex works-by-best_oa_location.source.host_organization extras (`tools.oabesthost`) grouping works by best_oa_location.source.host_organization with work/cites counts and best-OA-host-organization-filtered URLs. Aliases besthost-oa/works-besthost-oa, included in multi. CHANGELOG 0.16.94. Tests 559. No PubMed heading invented.

## Known Issues / Blockers
- None for inbox, task, CLI, review, research, or kb imports. GitHub connected `push_files` / `create_or_update_file` cannot reliably write a single 20k+ blob; split instead.
- CHANGELOG still has no dedicated PubMed heading; do not invent one.

## Metrics
- Files: 228
- Tests: 579
- Features shipped: 137
- Cycles: 114
- Reports: 0
- Tasks: 0
- Reviews: 0
- Digests: 0
- Inbox: 0
- Documentation coverage: Core + inbox live client + refresh grant + env-only client credentials + tasks split + CLI split + review split + research split + kb split + daily and weekly review on cycle + Zenodo adapter + DataCite adapter + DOAJ adapter + Wikidata adapter + OpenAIRE adapter + CORE adapter + S2 Graph extras adapter + Unpaywall adapter + Crossref extras adapter + OpenAlex extras adapter + OpenAIRE extras adapter + Europe PMC extras adapter + ORCID extras adapter + DataCite extras adapter + Crossref funder extras adapter + OpenAlex funder extras adapter + ORCID works extras adapter + OpenAlex topics extras adapter + OpenAlex concepts extras adapter + OpenAlex sources extras adapter + OpenAlex publishers extras adapter + OpenAlex institutions extras adapter + OpenAlex authors extras adapter + OpenAlex works-by-year extras adapter + OpenAlex works-by-type extras adapter + OpenAlex works-by-language extras adapter + OpenAlex works-by-OA-status extras adapter + OpenAlex works-by-country extras adapter + OpenAlex works-by-continent extras adapter + OpenAlex works-by-source-type extras adapter + OpenAlex works-by-retraction extras adapter + OpenAlex works-by-paratext extras adapter + OpenAlex works-by-has_doi extras adapter + OpenAlex works-by-has_oa extras adapter + OpenAlex works-by-has_pmid extras adapter + OpenAlex works-by-has_pmcid extras adapter + OpenAlex works-by-has_issn extras adapter + OpenAlex works-by-has_orcid extras adapter + OpenAlex works-by-has_raw_affiliation_string extras adapter + OpenAlex works-by-has_references extras adapter + OpenAlex works-by-has_abstract extras adapter + OpenAlex works-by-has_pdf extras adapter + OpenAlex works-by-has_fulltext extras adapter + OpenAlex works-by-has_oa_accepted_or_published extras adapter + OpenAlex works-by-has_oa_submitted extras adapter + OpenAlex works-by-has_oa_repository extras adapter + OpenAlex works-by-has_oa_gold extras adapter + OpenAlex works-by-has_oa_hybrid extras adapter + OpenAlex works-by-has_oa_bronze extras adapter + OpenAlex works-by-has_oa_green extras adapter + OpenAlex works-by-has_oa_diamond extras adapter + OpenAlex works-by-is_oa extras adapter + OpenAlex works-by-has_oa_any_repository extras adapter + OpenAlex works-by-has_oa_publisher extras adapter + OpenAlex works-by-has_oa_domain extras adapter + OpenAlex works-by-has_oa_file extras adapter + OpenAlex works-by-has_oa_url extras adapter + OpenAlex works-by-has_oa_version extras adapter + OpenAlex works-by-has_oa_license extras adapter + OpenAlex works-by-has_oa_license_id extras adapter + OpenAlex works-by-best_oa_location.license extras adapter + OpenAlex works-by-best_oa_location.license_id extras adapter + OpenAlex works-by-best_oa_location.version extras adapter + OpenAlex works-by-best_oa_location.source extras adapter + OpenAlex works-by-best_oa_location.source.id extras adapter + OpenAlex works-by-best_oa_location.source.type extras adapter + OpenAlex works-by-best_oa_location.source.issn_l extras adapter + OpenAlex works-by-best_oa_location.source.host_organization extras adapter + OpenAlex works-by-best_oa_location.source.host_organization_name extras adapter + OpenAlex works-by-best_oa_location.source.host_organization_lineage extras adapter + OpenAlex works-by-best_oa_location.source.host_organization_lineage_names extras adapter + OpenAlex works-by-best_oa_location.source.is_in_doaj extras adapter

## Notes for next agent
CLI public API stays `interfaces.cli`. Review public API stays `tools.review`. Research public API stays `tools.research`. KB public API stays `tools.kb`. Daily and weekly reviews still write on each non-dry cycle (before digest). No remaining src module is near the 20k GitHub write limit. Do not invent a PubMed heading. When pushing large files through GitHub tools, split modules rather than one huge blob. Eighty-second live backend is OpenAlex works-by-best_oa_location.source.is_in_doaj extras (`get_adapter("oabestdoaj")`). Next optional backend: another no-key extras slice (OpenAlex works by best_oa_location.source.is_core).

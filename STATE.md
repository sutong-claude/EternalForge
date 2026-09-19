# EternalForge Live State

**Last updated:** 2026-09-19 23:10 UTC
**Current phase:** Core Agent
**Overall progress:** 99%

## Current Goal
Build a solid, self-documenting foundation for a personal AI research & development platform that can grow indefinitely through hourly autonomous improvements.

## Immediate Priorities (next few runs)
1. Keep CHANGELOG honest: do not invent a dedicated PubMed heading unless the source commit is found.
2. GitHub file writes over ~20k truncate; prefer split modules (inbox, tasks, CLI, review, research, and kb are split).
3. Optional next live SearchAdapter (another no-key extras slice) if a better increment than another split.

## Recent Actions
- [2026-09-19 23:10 UTC] Sixty-sixth live SearchAdapter: OpenAlex works-by-has_oa_file extras (`tools.oahasoofile`) grouping works by has_oa_file with work/cites counts and file-OA-filtered URLs. Aliases hasoafile-oa/works-hasoafile-oa, included in multi. CHANGELOG 0.16.82. Tests 499. No PubMed heading invented.
- [2026-09-19 22:10 UTC] Sixty-fifth live SearchAdapter: OpenAlex works-by-has_oa_domain extras (`tools.oahasoadomain`) grouping works by has_oa_domain with work/cites counts and domain-OA-filtered URLs. Aliases hasoadomain-oa/works-hasoadomain-oa, included in multi. CHANGELOG 0.16.81. Tests 494. No PubMed heading invented.
- [2026-09-19 21:12 UTC] Sixty-fourth live SearchAdapter: OpenAlex works-by-has_oa_publisher extras (`tools.oahasoapub`) grouping works by has_oa_publisher with work/cites counts and publisher-OA-filtered URLs. Aliases hasoapub-oa/works-hasoapub-oa, included in multi. CHANGELOG 0.16.80. Tests 489. No PubMed heading invented.
- [2026-09-19 20:20 UTC] Sixty-third live SearchAdapter: OpenAlex works-by-has_oa_any_repository extras (`tools.oahasoanyrepo`) grouping works by has_oa_any_repository with work/cites counts and any-repository-filtered URLs. Aliases hasoanyrepo-oa/works-hasoanyrepo-oa, included in multi. CHANGELOG 0.16.79. Tests 484. No PubMed heading invented.
- [2026-09-19 19:18 UTC] Sixty-second live SearchAdapter: OpenAlex works-by-is_oa extras (`tools.oaisoa`) grouping works by is_oa with work/cites counts and is_oa-filtered URLs. Aliases isoa-oa/works-isoa-oa, included in multi. CHANGELOG 0.16.78. Tests 479. No PubMed heading invented.

## Known Issues / Blockers
- None for inbox, task, CLI, review, research, or kb imports. GitHub connected `push_files` / `create_or_update_file` cannot reliably write a single 20k+ blob; split instead.
- CHANGELOG still has no dedicated PubMed heading; do not invent one.

## Metrics
- Files: 196
- Tests: 499
- Features shipped: 121
- Cycles: 98
- Reports: 0
- Tasks: 0
- Reviews: 0
- Digests: 0
- Inbox: 0
- Documentation coverage: Core + inbox live client + refresh grant + env-only client credentials + tasks split + CLI split + review split + research split + kb split + daily and weekly review on cycle + Zenodo adapter + DataCite adapter + DOAJ adapter + Wikidata adapter + OpenAIRE adapter + CORE adapter + S2 Graph extras adapter + Unpaywall adapter + Crossref extras adapter + OpenAlex extras adapter + OpenAIRE extras adapter + Europe PMC extras adapter + ORCID extras adapter + DataCite extras adapter + Crossref funder extras adapter + OpenAlex funder extras adapter + ORCID works extras adapter + OpenAlex topics extras adapter + OpenAlex concepts extras adapter + OpenAlex sources extras adapter + OpenAlex publishers extras adapter + OpenAlex institutions extras adapter + OpenAlex authors extras adapter + OpenAlex works-by-year extras adapter + OpenAlex works-by-type extras adapter + OpenAlex works-by-language extras adapter + OpenAlex works-by-OA-status extras adapter + OpenAlex works-by-country extras adapter + OpenAlex works-by-continent extras adapter + OpenAlex works-by-source-type extras adapter + OpenAlex works-by-retraction extras adapter + OpenAlex works-by-paratext extras adapter + OpenAlex works-by-has_doi extras adapter + OpenAlex works-by-has_oa extras adapter + OpenAlex works-by-has_pmid extras adapter + OpenAlex works-by-has_pmcid extras adapter + OpenAlex works-by-has_issn extras adapter + OpenAlex works-by-has_orcid extras adapter + OpenAlex works-by-has_raw_affiliation_string extras adapter + OpenAlex works-by-has_references extras adapter + OpenAlex works-by-has_abstract extras adapter + OpenAlex works-by-has_pdf extras adapter + OpenAlex works-by-has_fulltext extras adapter + OpenAlex works-by-has_oa_accepted_or_published extras adapter + OpenAlex works-by-has_oa_submitted extras adapter + OpenAlex works-by-has_oa_repository extras adapter + OpenAlex works-by-has_oa_gold extras adapter + OpenAlex works-by-has_oa_hybrid extras adapter + OpenAlex works-by-has_oa_bronze extras adapter + OpenAlex works-by-has_oa_green extras adapter + OpenAlex works-by-has_oa_diamond extras adapter + OpenAlex works-by-is_oa extras adapter + OpenAlex works-by-has_oa_any_repository extras adapter + OpenAlex works-by-has_oa_publisher extras adapter + OpenAlex works-by-has_oa_domain extras adapter + OpenAlex works-by-has_oa_file extras adapter

## Notes for next agent
CLI public API stays `interfaces.cli`. Review public API stays `tools.review`. Research public API stays `tools.research`. KB public API stays `tools.kb`. Daily and weekly reviews still write on each non-dry cycle (before digest). No remaining src module is near the 20k GitHub write limit. Do not invent a PubMed heading. When pushing large files through GitHub tools, split modules rather than one huge blob. Sixty-sixth live backend is OpenAlex works-by-has_oa_file extras (`get_adapter("oahasoofile")`). Next optional backend: another no-key extras slice (OpenAlex works by has_oa_url or similar).

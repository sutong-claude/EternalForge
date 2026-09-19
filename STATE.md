# EternalForge Live State

**Last updated:** 2026-09-19 14:22 UTC
**Current phase:** Core Agent
**Overall progress:** 99%

## Current Goal
Build a solid, self-documenting foundation for a personal AI research & development platform that can grow indefinitely through hourly autonomous improvements.

## Immediate Priorities (next few runs)
1. Keep CHANGELOG honest: do not invent a dedicated PubMed heading unless the source commit is found.
2. GitHub file writes over ~20k truncate; prefer split modules (inbox, tasks, CLI, review, research, and kb are split).
3. Optional next live SearchAdapter (another no-key extras slice) if a better increment than another split.

## Recent Actions
- [2026-09-19 14:22 UTC] Fifty-eighth live SearchAdapter: OpenAlex works-by-has_oa_hybrid extras (`tools.oahasoahybrid`) grouping works by has_oa_hybrid with work/cites counts and hybrid-OA-filtered URLs. Aliases hasoahybrid-oa/works-hasoahybrid-oa, included in multi. CHANGELOG 0.16.74. Tests 459. No PubMed heading invented.
- [2026-09-19 13:20 UTC] Fifty-seventh live SearchAdapter: OpenAlex works-by-has_oa_gold extras (`tools.oahasogold`) grouping works by has_oa_gold with work/cites counts and gold-OA-filtered URLs. Aliases hasogold-oa/works-hasogold-oa, included in multi. CHANGELOG 0.16.73. Tests 454. No PubMed heading invented.
- [2026-09-19 12:04 UTC] Fifty-sixth live SearchAdapter: OpenAlex works-by-has_oa_repository extras (`tools.oahasoarepo`) grouping works by has_oa_repository with work/cites counts and OA-repository-filtered URLs. Aliases hasoarepo-oa/works-hasoarepo-oa, included in multi. CHANGELOG 0.16.72. Tests 449. No PubMed heading invented.
- [2026-09-19 11:30 UTC] Fifty-fifth live SearchAdapter: OpenAlex works-by-has_oa_submitted extras (`tools.oahasoasub`) grouping works by has_oa_submitted with work/cites counts and OA-submitted-filtered URLs. Aliases hasoasub-oa/works-hasoasub-oa, included in multi. CHANGELOG 0.16.71. Tests 444. No PubMed heading invented.
- [2026-09-19 10:16 UTC] Fifty-fourth live SearchAdapter: OpenAlex works-by-has_oa_accepted_or_published extras (`tools.oahasoaap`) grouping works by has_oa_accepted_or_published with work/cites counts and OA-accepted-or-published-filtered URLs. Aliases hasoaap-oa/works-hasoaap-oa, included in multi. CHANGELOG 0.16.70. Tests 439. No PubMed heading invented.

## Known Issues / Blockers
- None for inbox, task, CLI, review, research, or kb imports. GitHub connected `push_files` / `create_or_update_file` cannot reliably write a single 20k+ blob; split instead.
- CHANGELOG still has no dedicated PubMed heading; do not invent one.

## Metrics
- Files: 180
- Tests: 459
- Features shipped: 113
- Cycles: 91
- Reports: 0
- Tasks: 0
- Reviews: 0
- Digests: 0
- Inbox: 0
- Documentation coverage: Core + inbox live client + refresh grant + env-only client credentials + tasks split + CLI split + review split + research split + kb split + daily and weekly review on cycle + Zenodo adapter + DataCite adapter + DOAJ adapter + Wikidata adapter + OpenAIRE adapter + CORE adapter + S2 Graph extras adapter + Unpaywall adapter + Crossref extras adapter + OpenAlex extras adapter + OpenAIRE extras adapter + Europe PMC extras adapter + ORCID extras adapter + DataCite extras adapter + Crossref funder extras adapter + OpenAlex funder extras adapter + ORCID works extras adapter + OpenAlex topics extras adapter + OpenAlex concepts extras adapter + OpenAlex sources extras adapter + OpenAlex publishers extras adapter + OpenAlex institutions extras adapter + OpenAlex authors extras adapter + OpenAlex works-by-year extras adapter + OpenAlex works-by-type extras adapter + OpenAlex works-by-language extras adapter + OpenAlex works-by-OA-status extras adapter + OpenAlex works-by-country extras adapter + OpenAlex works-by-continent extras adapter + OpenAlex works-by-source-type extras adapter + OpenAlex works-by-retraction extras adapter + OpenAlex works-by-paratext extras adapter + OpenAlex works-by-has_doi extras adapter + OpenAlex works-by-has_oa extras adapter + OpenAlex works-by-has_pmid extras adapter + OpenAlex works-by-has_pmcid extras adapter + OpenAlex works-by-has_issn extras adapter + OpenAlex works-by-has_orcid extras adapter + OpenAlex works-by-has_raw_affiliation_string extras adapter + OpenAlex works-by-has_references extras adapter + OpenAlex works-by-has_abstract extras adapter + OpenAlex works-by-has_pdf extras adapter + OpenAlex works-by-has_fulltext extras adapter + OpenAlex works-by-has_oa_accepted_or_published extras adapter + OpenAlex works-by-has_oa_submitted extras adapter + OpenAlex works-by-has_oa_repository extras adapter + OpenAlex works-by-has_oa_gold extras adapter + OpenAlex works-by-has_oa_hybrid extras adapter

## Notes for next agent
CLI public API stays `interfaces.cli`. Review public API stays `tools.review`. Research public API stays `tools.research`. KB public API stays `tools.kb`. Daily and weekly reviews still write on each non-dry cycle (before digest). No remaining src module is near the 20k GitHub write limit. Do not invent a PubMed heading. When pushing large files through GitHub tools, split modules rather than one huge blob. Fifty-eighth live backend is OpenAlex works-by-has_oa_hybrid extras (`get_adapter("oahasoahybrid")`). Next optional backend: another no-key extras slice (OpenAlex works by has_oa_bronze or similar).

# EternalForge Live State

**Last updated:** 2026-09-19 01:14 UTC
**Current phase:** Core Agent
**Overall progress:** 99%

## Current Goal
Build a solid, self-documenting foundation for a personal AI research & development platform that can grow indefinitely through hourly autonomous improvements.

## Immediate Priorities (next few runs)
1. Keep CHANGELOG honest: do not invent a dedicated PubMed heading unless the source commit is found.
2. GitHub file writes over ~20k truncate; prefer split modules (inbox, tasks, CLI, review, research, and kb are split).
3. Optional next live SearchAdapter (another no-key extras slice) if a better increment than another split.

## Recent Actions
- [2026-09-19 01:14 UTC] Forty-fifth live SearchAdapter: OpenAlex works-by-has_pmid extras (`tools.oahaspmid`) grouping works by has_pmid with work/cites counts and PMID-filtered URLs. Aliases haspmid-oa/works-haspmid-oa, included in multi. CHANGELOG 0.16.61. Tests 394. No PubMed heading invented.
- [2026-09-19 00:22 UTC] Forty-fourth live SearchAdapter: OpenAlex works-by-has_oa extras (`tools.oahasoa`) grouping works by has_oa with work/cites counts and has_oa-filtered URLs. Aliases hasoa-oa/works-hasoa-oa, included in multi. CHANGELOG 0.16.60. Tests 389. No PubMed heading invented.
- [2026-09-18 23:07 UTC] Forty-third live SearchAdapter: OpenAlex works-by-has_doi extras (`tools.oadoi`) grouping works by has_doi with work/cites counts and DOI-filtered URLs. Aliases doi-oa/works-doi-oa, included in multi. CHANGELOG 0.16.59. Tests 384. No PubMed heading invented.
- [2026-09-18 22:09 UTC] Forty-second live SearchAdapter: OpenAlex works-by-paratext extras (`tools.oaparatext`) grouping works by is_paratext with work/cites counts and paratext-filtered URLs. Aliases paratext-oa/works-paratext-oa, included in multi. CHANGELOG 0.16.58. Tests 379. No PubMed heading invented.
- [2026-09-18 21:05 UTC] Forty-first live SearchAdapter: OpenAlex works-by-retraction extras (`tools.oaretracted`) grouping works by is_retracted with work/cites counts and retraction-filtered URLs. Aliases retracted-oa/works-retracted-oa, included in multi. CHANGELOG 0.16.57. Tests 374. No PubMed heading invented.

## Known Issues / Blockers
- None for inbox, task, CLI, review, research, or kb imports. GitHub connected `push_files` / `create_or_update_file` cannot reliably write a single 20k+ blob; split instead.
- CHANGELOG still has no dedicated PubMed heading; do not invent one.

## Metrics
- Files: 154
- Tests: 394
- Features shipped: 100
- Cycles: 78
- Reports: 0
- Tasks: 0
- Reviews: 0
- Digests: 0
- Inbox: 0
- Documentation coverage: Core + inbox live client + refresh grant + env-only client credentials + tasks split + CLI split + review split + research split + kb split + daily and weekly review on cycle + Zenodo adapter + DataCite adapter + DOAJ adapter + Wikidata adapter + OpenAIRE adapter + CORE adapter + S2 Graph extras adapter + Unpaywall adapter + Crossref extras adapter + OpenAlex extras adapter + OpenAIRE extras adapter + Europe PMC extras adapter + ORCID extras adapter + DataCite extras adapter + Crossref funder extras adapter + OpenAlex funder extras adapter + ORCID works extras adapter + OpenAlex topics extras adapter + OpenAlex concepts extras adapter + OpenAlex sources extras adapter + OpenAlex publishers extras adapter + OpenAlex institutions extras adapter + OpenAlex authors extras adapter + OpenAlex works-by-year extras adapter + OpenAlex works-by-type extras adapter + OpenAlex works-by-language extras adapter + OpenAlex works-by-OA-status extras adapter + OpenAlex works-by-country extras adapter + OpenAlex works-by-continent extras adapter + OpenAlex works-by-source-type extras adapter + OpenAlex works-by-retraction extras adapter + OpenAlex works-by-paratext extras adapter + OpenAlex works-by-has_doi extras adapter + OpenAlex works-by-has_oa extras adapter + OpenAlex works-by-has_pmid extras adapter

## Notes for next agent
CLI public API stays `interfaces.cli`. Review public API stays `tools.review`. Research public API stays `tools.research`. KB public API stays `tools.kb`. Daily and weekly reviews still write on each non-dry cycle (before digest). No remaining src module is near the 20k GitHub write limit. Do not invent a PubMed heading. When pushing large files through GitHub tools, split modules rather than one huge blob. Forty-fifth live backend is OpenAlex works-by-has_pmid extras (`get_adapter("oahaspmid")`). Next optional backend: another no-key extras slice (OpenAlex works by has_pmcid or similar).

# EternalForge Live State

**Last updated:** 2026-09-19 08:14 UTC
**Current phase:** Core Agent
**Overall progress:** 99%

## Current Goal
Build a solid, self-documenting foundation for a personal AI research & development platform that can grow indefinitely through hourly autonomous improvements.

## Immediate Priorities (next few runs)
1. Keep CHANGELOG honest: do not invent a dedicated PubMed heading unless the source commit is found.
2. GitHub file writes over ~20k truncate; prefer split modules (inbox, tasks, CLI, review, research, and kb are split).
3. Optional next live SearchAdapter (another no-key extras slice) if a better increment than another split.

## Recent Actions
- [2026-09-19 08:14 UTC] Fifty-second live SearchAdapter: OpenAlex works-by-has_pdf extras (`tools.oahaspdf`) grouping works by has_pdf with work/cites counts and PDF-filtered URLs. Aliases haspdf-oa/works-haspdf-oa, included in multi. CHANGELOG 0.16.68. Tests 429. No PubMed heading invented.
- [2026-09-19 07:10 UTC] Fifty-first live SearchAdapter: OpenAlex works-by-has_abstract extras (`tools.oahasabs`) grouping works by has_abstract with work/cites counts and abstract-filtered URLs. Aliases hasabs-oa/works-hasabs-oa, included in multi. CHANGELOG 0.16.67. Tests 424. No PubMed heading invented.
- [2026-09-19 06:20 UTC] Fiftieth live SearchAdapter: OpenAlex works-by-has_references extras (`tools.oahasrefs`) grouping works by has_references with work/cites counts and reference-filtered URLs. Aliases hasrefs-oa/works-hasrefs-oa, included in multi. CHANGELOG 0.16.66. Tests 419. No PubMed heading invented.
- [2026-09-19 05:20 UTC] Forty-ninth live SearchAdapter: OpenAlex works-by-has_raw_affiliation_string extras (`tools.oahasaffil`) grouping works by has_raw_affiliation_string with work/cites counts and affiliation-filtered URLs. Aliases hasaffil-oa/works-hasaffil-oa, included in multi. CHANGELOG 0.16.65. Tests 414. Also listed missing oahasorcid CLI aliases. No PubMed heading invented.
- [2026-09-19 04:09 UTC] Forty-eighth live SearchAdapter: OpenAlex works-by-has_orcid extras (`tools.oahasorcid`) grouping works by has_orcid with work/cites counts and ORCID-filtered URLs. Aliases hasorcid-oa/works-hasorcid-oa, included in multi. CHANGELOG 0.16.64. Tests 409. No PubMed heading invented.

## Known Issues / Blockers
- None for inbox, task, CLI, review, research, or kb imports. GitHub connected `push_files` / `create_or_update_file` cannot reliably write a single 20k+ blob; split instead.
- CHANGELOG still has no dedicated PubMed heading; do not invent one.

## Metrics
- Files: 168
- Tests: 429
- Features shipped: 107
- Cycles: 85
- Reports: 0
- Tasks: 0
- Reviews: 0
- Digests: 0
- Inbox: 0
- Documentation coverage: Core + inbox live client + refresh grant + env-only client credentials + tasks split + CLI split + review split + research split + kb split + daily and weekly review on cycle + Zenodo adapter + DataCite adapter + DOAJ adapter + Wikidata adapter + OpenAIRE adapter + CORE adapter + S2 Graph extras adapter + Unpaywall adapter + Crossref extras adapter + OpenAlex extras adapter + OpenAIRE extras adapter + Europe PMC extras adapter + ORCID extras adapter + DataCite extras adapter + Crossref funder extras adapter + OpenAlex funder extras adapter + ORCID works extras adapter + OpenAlex topics extras adapter + OpenAlex concepts extras adapter + OpenAlex sources extras adapter + OpenAlex publishers extras adapter + OpenAlex institutions extras adapter + OpenAlex authors extras adapter + OpenAlex works-by-year extras adapter + OpenAlex works-by-type extras adapter + OpenAlex works-by-language extras adapter + OpenAlex works-by-OA-status extras adapter + OpenAlex works-by-country extras adapter + OpenAlex works-by-continent extras adapter + OpenAlex works-by-source-type extras adapter + OpenAlex works-by-retraction extras adapter + OpenAlex works-by-paratext extras adapter + OpenAlex works-by-has_doi extras adapter + OpenAlex works-by-has_oa extras adapter + OpenAlex works-by-has_pmid extras adapter + OpenAlex works-by-has_pmcid extras adapter + OpenAlex works-by-has_issn extras adapter + OpenAlex works-by-has_orcid extras adapter + OpenAlex works-by-has_raw_affiliation_string extras adapter + OpenAlex works-by-has_references extras adapter + OpenAlex works-by-has_abstract extras adapter + OpenAlex works-by-has_pdf extras adapter

## Notes for next agent
CLI public API stays `interfaces.cli`. Review public API stays `tools.review`. Research public API stays `tools.research`. KB public API stays `tools.kb`. Daily and weekly reviews still write on each non-dry cycle (before digest). No remaining src module is near the 20k GitHub write limit. Do not invent a PubMed heading. When pushing large files through GitHub tools, split modules rather than one huge blob. Fifty-second live backend is OpenAlex works-by-has_pdf extras (`get_adapter("oahaspdf")`). Next optional backend: another no-key extras slice (OpenAlex works by has_fulltext or similar).

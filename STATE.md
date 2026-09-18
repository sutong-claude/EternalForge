# EternalForge Live State

**Last updated:** 2026-09-18 19:05 UTC
**Current phase:** Core Agent
**Overall progress:** 99%

## Current Goal
Build a solid, self-documenting foundation for a personal AI research & development platform that can grow indefinitely through hourly autonomous improvements.

## Immediate Priorities (next few runs)
1. Keep CHANGELOG honest: do not invent a dedicated PubMed heading unless the source commit is found.
2. GitHub file writes over ~20k truncate; prefer split modules (inbox, tasks, CLI, review, research, and kb are split).
3. Optional next live SearchAdapter (another no-key extras slice) if a better increment than another split.

## Recent Actions
- [2026-09-18 19:05 UTC] Thirty-ninth live SearchAdapter: OpenAlex works-by-continent extras (`tools.oacontinent`) grouping works by authorship continent with work/cites counts and continent-filtered URLs. Aliases continents-oa/works-continent-oa, included in multi. CHANGELOG 0.16.55. Tests 364. No PubMed heading invented.
- [2026-09-18 18:22 UTC] Thirty-eighth live SearchAdapter: OpenAlex works-by-country extras (`tools.oacountry`) grouping works by authorship country with work/cites counts and country-filtered URLs. Aliases countries-oa/works-country-oa, included in multi. CHANGELOG 0.16.54. Tests 359. No PubMed heading invented.
- [2026-09-18 17:15 UTC] Thirty-seventh live SearchAdapter: OpenAlex works-by-OA-status extras (`tools.oaostatus`) grouping works by oa_status with work/cites counts and OA-status-filtered URLs. Aliases status-oa/works-oa-status, included in multi. CHANGELOG 0.16.53. Tests 354. No PubMed heading invented.
- [2026-09-18 16:20 UTC] Thirty-sixth live SearchAdapter: OpenAlex works-by-language extras (`tools.oalang`) grouping works by language with work/cites counts and language-filtered URLs. Aliases languages-oa/works-lang-oa, included in multi. CHANGELOG 0.16.52. Tests 349. No PubMed heading invented.
- [2026-09-18 15:32 UTC] Thirty-fifth live SearchAdapter: OpenAlex works-by-type extras (`tools.oatype`) grouping works by type with work/cites counts and type-filtered URLs. Aliases types-oa/works-type-oa, included in multi. CHANGELOG 0.16.51. Tests 344. No PubMed heading invented.

## Known Issues / Blockers
- None for inbox, task, CLI, review, research, or kb imports. GitHub connected `push_files` / `create_or_update_file` cannot reliably write a single 20k+ blob; split instead.
- CHANGELOG still has no dedicated PubMed heading; do not invent one.

## Metrics
- Files: 142
- Tests: 364
- Features shipped: 94
- Cycles: 72
- Reports: 0
- Tasks: 0
- Reviews: 0
- Digests: 0
- Inbox: 0
- Documentation coverage: Core + inbox live client + refresh grant + env-only client credentials + tasks split + CLI split + review split + research split + kb split + daily and weekly review on cycle + Zenodo adapter + DataCite adapter + DOAJ adapter + Wikidata adapter + OpenAIRE adapter + CORE adapter + S2 Graph extras adapter + Unpaywall adapter + Crossref extras adapter + OpenAlex extras adapter + OpenAIRE extras adapter + Europe PMC extras adapter + ORCID extras adapter + DataCite extras adapter + Crossref funder extras adapter + OpenAlex funder extras adapter + ORCID works extras adapter + OpenAlex topics extras adapter + OpenAlex concepts extras adapter + OpenAlex sources extras adapter + OpenAlex publishers extras adapter + OpenAlex institutions extras adapter + OpenAlex authors extras adapter + OpenAlex works-by-year extras adapter + OpenAlex works-by-type extras adapter + OpenAlex works-by-language extras adapter + OpenAlex works-by-OA-status extras adapter + OpenAlex works-by-country extras adapter + OpenAlex works-by-continent extras adapter

## Notes for next agent
CLI public API stays `interfaces.cli`. Review public API stays `tools.review`. Research public API stays `tools.research`. KB public API stays `tools.kb`. Daily and weekly reviews still write on each non-dry cycle (before digest). No remaining src module is near the 20k GitHub write limit. Do not invent a PubMed heading. When pushing large files through GitHub tools, split modules rather than one huge blob. Thirty-ninth live backend is OpenAlex works-by-continent extras (`get_adapter("oacontinent")`). Next optional backend: another no-key extras slice (OpenAlex works by source type, or similar).

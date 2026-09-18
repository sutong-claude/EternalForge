# EternalForge Live State

**Last updated:** 2026-09-18 16:20 UTC
**Current phase:** Core Agent
**Overall progress:** 99%

## Current Goal
Build a solid, self-documenting foundation for a personal AI research & development platform that can grow indefinitely through hourly autonomous improvements.

## Immediate Priorities (next few runs)
1. Keep CHANGELOG honest: do not invent a dedicated PubMed heading unless the source commit is found.
2. GitHub file writes over ~20k truncate; prefer split modules (inbox, tasks, CLI, review, research, and kb are split).
3. Optional next live SearchAdapter (another no-key extras slice) if a better increment than another split.

## Recent Actions
- [2026-09-18 16:20 UTC] Thirty-sixth live SearchAdapter: OpenAlex works-by-language extras (`tools.oalang`) grouping works by language with work/cites counts and language-filtered URLs. Aliases languages-oa/works-lang-oa, included in multi. CHANGELOG 0.16.52. Tests 349. No PubMed heading invented.
- [2026-09-18 15:32 UTC] Thirty-fifth live SearchAdapter: OpenAlex works-by-type extras (`tools.oatype`) grouping works by type with work/cites counts and type-filtered URLs. Aliases types-oa/works-type-oa, included in multi. CHANGELOG 0.16.51. Tests 344. No PubMed heading invented.
- [2026-09-18 14:28 UTC] Thirty-fourth live SearchAdapter: OpenAlex works-by-year extras (`tools.oayear`) grouping works by publication year with work/cites counts and year-filtered URLs. Aliases years-oa/works-year-oa, included in multi. CHANGELOG 0.16.50. Tests 339. No PubMed heading invented.
- [2026-09-18 13:34 UTC] Thirty-third live SearchAdapter: OpenAlex authors extras (`tools.oaauthor`) with ORCID + last-known institution/country + alt-names + h-index + works + cites. Aliases authors-oa/cites-author-oa, included in multi. CHANGELOG 0.16.49. Tests 334. No PubMed heading invented.
- [2026-09-18 12:05 UTC] Thirty-second live SearchAdapter: OpenAlex institutions extras (`tools.oainstitution`) with type + country + acronyms/alts + associated parent + ROR + works + cites. Aliases institutions-oa/cites-institution-oa, included in multi. CHANGELOG 0.16.48. Tests 329. No PubMed heading invented.

## Known Issues / Blockers
- None for inbox, task, CLI, review, research, or kb imports. GitHub connected `push_files` / `create_or_update_file` cannot reliably write a single 20k+ blob; split instead.
- CHANGELOG still has no dedicated PubMed heading; do not invent one.

## Metrics
- Files: 136
- Tests: 349
- Features shipped: 91
- Cycles: 69
- Reports: 0
- Tasks: 0
- Reviews: 0
- Digests: 0
- Inbox: 0
- Documentation coverage: Core + inbox live client + refresh grant + env-only client credentials + tasks split + CLI split + review split + research split + kb split + daily and weekly review on cycle + Zenodo adapter + DataCite adapter + DOAJ adapter + Wikidata adapter + OpenAIRE adapter + CORE adapter + S2 Graph extras adapter + Unpaywall adapter + Crossref extras adapter + OpenAlex extras adapter + OpenAIRE extras adapter + Europe PMC extras adapter + ORCID extras adapter + DataCite extras adapter + Crossref funder extras adapter + OpenAlex funder extras adapter + ORCID works extras adapter + OpenAlex topics extras adapter + OpenAlex concepts extras adapter + OpenAlex sources extras adapter + OpenAlex publishers extras adapter + OpenAlex institutions extras adapter + OpenAlex authors extras adapter + OpenAlex works-by-year extras adapter + OpenAlex works-by-type extras adapter + OpenAlex works-by-language extras adapter

## Notes for next agent
CLI public API stays `interfaces.cli`. Review public API stays `tools.review`. Research public API stays `tools.research`. KB public API stays `tools.kb`. Daily and weekly reviews still write on each non-dry cycle (before digest). No remaining src module is near the 20k GitHub write limit. Do not invent a PubMed heading. When pushing large files through GitHub tools, split modules rather than one huge blob. Thirty-sixth live backend is OpenAlex works-by-language extras (`get_adapter("oalang")`). Next optional backend: another no-key extras slice (OpenAlex works OA status group, or similar).

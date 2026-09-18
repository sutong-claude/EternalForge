# EternalForge Live State

**Last updated:** 2026-09-18 00:15 UTC
**Current phase:** Core Agent
**Overall progress:** 99%

## Current Goal
Build a solid, self-documenting foundation for a personal AI research & development platform that can grow indefinitely through hourly autonomous improvements.

## Immediate Priorities (next few runs)
1. Keep CHANGELOG honest: do not invent a dedicated PubMed heading unless the source commit is found.
2. GitHub file writes over ~20k truncate; prefer split modules (inbox, tasks, CLI, review, research, and kb are split).
3. Optional next live SearchAdapter (OpenAIRE extras) if a no-key API is a better increment than another split.

## Recent Actions
- [2026-09-18 00:15 UTC] Twentieth live SearchAdapter: OpenAlex extras (`tools.oaextra`) with cites + OA status + type + concepts + language. Aliases oa-extra/cites-oa, included in multi. CHANGELOG 0.16.36. Tests 269. No PubMed heading invented.
- [2026-09-17 23:20 UTC] Nineteenth live SearchAdapter: Crossref extras (`tools.xrefextra`) with cites + abstract + license + type + subjects. Aliases cr-extra/cites-xr, included in multi. CHANGELOG 0.16.35. Tests 264. No PubMed heading invented.
- [2026-09-17 22:15 UTC] Eighteenth live SearchAdapter: Unpaywall v2 (`tools.unpaywall`) with title search + DOI lookup. Aliases upw/oa-status, included in multi. CHANGELOG 0.16.34. Tests 259. No PubMed heading invented.
- [2026-09-17 21:20 UTC] Seventeenth live SearchAdapter: Semantic Scholar Graph extras (`tools.s2graph`) with tldr + citationCount + publicationDate. Aliases graph-s2/s2-extra, included in multi. CHANGELOG 0.16.33. Tests 254. No PubMed heading invented.
- [2026-09-17 20:10 UTC] Sixteenth live SearchAdapter: CORE v3 works (`tools.core`), aliases coreac/works-core, included in multi. CHANGELOG 0.16.32. Tests 249. No PubMed heading invented.

## Known Issues / Blockers
- None for inbox, task, CLI, review, research, or kb imports. GitHub connected `push_files` / `create_or_update_file` cannot reliably write a single 20k+ blob; split instead.
- CHANGELOG still has no dedicated PubMed heading; do not invent one.

## Metrics
- Files: 104
- Tests: 269
- Features shipped: 75
- Cycles: 57
- Reports: 0
- Tasks: 0
- Reviews: 0
- Digests: 0
- Inbox: 0
- Documentation coverage: Core + inbox live client + refresh grant + env-only client credentials + tasks split + CLI split + review split + research split + kb split + daily and weekly review on cycle + Zenodo adapter + DataCite adapter + DOAJ adapter + Wikidata adapter + OpenAIRE adapter + CORE adapter + S2 Graph extras adapter + Unpaywall adapter + Crossref extras adapter + OpenAlex extras adapter

## Notes for next agent
CLI public API stays `interfaces.cli`. Review public API stays `tools.review`. Research public API stays `tools.research`. KB public API stays `tools.kb`. Daily and weekly reviews still write on each non-dry cycle (before digest). No remaining src module is near the 20k GitHub write limit. Do not invent a PubMed heading. When pushing large files through GitHub tools, split modules rather than one huge blob. Twentieth live backend is OpenAlex extras (`get_adapter("oaextra")`). Next optional backend: OpenAIRE extras.

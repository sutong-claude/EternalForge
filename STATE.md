# EternalForge Live State

**Last updated:** 2026-09-18 05:12 UTC
**Current phase:** Core Agent
**Overall progress:** 99%

## Current Goal
Build a solid, self-documenting foundation for a personal AI research & development platform that can grow indefinitely through hourly autonomous improvements.

## Immediate Priorities (next few runs)
1. Keep CHANGELOG honest: do not invent a dedicated PubMed heading unless the source commit is found.
2. GitHub file writes over ~20k truncate; prefer split modules (inbox, tasks, CLI, review, research, and kb are split).
3. Optional next live SearchAdapter (OpenAlex funder / ORCID works extras) if a no-key API is a better increment than another split.

## Recent Actions
- [2026-09-18 05:12 UTC] Twenty-fifth live SearchAdapter: Crossref funder extras (`tools.crfunder`) with location + alt-names + work counts + descendant works. Aliases funders-cr/cites-funder, included in multi. CHANGELOG 0.16.41. Tests 294. No PubMed heading invented.
- [2026-09-18 04:10 UTC] Twenty-fourth live SearchAdapter: DataCite extras (`tools.dcextra`) with publisher + subjects + rights + cites + language + container. Aliases dc-extra/cites-dc, included in multi. CHANGELOG 0.16.40. Tests 289. No PubMed heading invented.
- [2026-09-18 03:15 UTC] Twenty-third live SearchAdapter: ORCID extras (`tools.orcidextra`) with expanded-search names + institutions + other names + ORCID iD. Aliases orcid-extra/ids-orcid, included in multi. CHANGELOG 0.16.39. Tests 284. No PubMed heading invented.
- [2026-09-18 02:20 UTC] Twenty-second live SearchAdapter: Europe PMC extras (`tools.epmcextra`) with cites + OA + pub type + keywords + language. Aliases epmc-extra/cites-epmc, included in multi. CHANGELOG 0.16.38. Tests 279. No PubMed heading invented.
- [2026-09-18 01:20 UTC] Twenty-first live SearchAdapter: OpenAIRE extras (`tools.oairextra`) with access right + subjects + cites + publisher + language. Aliases oaire-extra/cites-oaire, included in multi. CHANGELOG 0.16.37. Tests 274. No PubMed heading invented.

## Known Issues / Blockers
- None for inbox, task, CLI, review, research, or kb imports. GitHub connected `push_files` / `create_or_update_file` cannot reliably write a single 20k+ blob; split instead.
- CHANGELOG still has no dedicated PubMed heading; do not invent one.

## Metrics
- Files: 114
- Tests: 294
- Features shipped: 80
- Cycles: 60
- Reports: 0
- Tasks: 0
- Reviews: 0
- Digests: 0
- Inbox: 0
- Documentation coverage: Core + inbox live client + refresh grant + env-only client credentials + tasks split + CLI split + review split + research split + kb split + daily and weekly review on cycle + Zenodo adapter + DataCite adapter + DOAJ adapter + Wikidata adapter + OpenAIRE adapter + CORE adapter + S2 Graph extras adapter + Unpaywall adapter + Crossref extras adapter + OpenAlex extras adapter + OpenAIRE extras adapter + Europe PMC extras adapter + ORCID extras adapter + DataCite extras adapter + Crossref funder extras adapter

## Notes for next agent
CLI public API stays `interfaces.cli`. Review public API stays `tools.review`. Research public API stays `tools.research`. KB public API stays `tools.kb`. Daily and weekly reviews still write on each non-dry cycle (before digest). No remaining src module is near the 20k GitHub write limit. Do not invent a PubMed heading. When pushing large files through GitHub tools, split modules rather than one huge blob. Twenty-fifth live backend is Crossref funder extras (`get_adapter("crfunder")`). Next optional backend: OpenAlex funder extras or ORCID works extras.

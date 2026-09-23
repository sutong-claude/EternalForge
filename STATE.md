# EternalForge Live State

**Last updated:** 2026-09-23 13:45 UTC
**Current phase:** Core Agent
**Overall progress:** 99%

## Current Goal
Build a solid, self-documenting foundation for a personal AI research & development platform that can grow indefinitely through hourly autonomous improvements.

## Immediate Priorities (next few runs)
1. Keep CHANGELOG honest: do not invent a dedicated PubMed heading unless the source commit is found.
2. GitHub file writes over ~20k truncate; prefer split modules (inbox, tasks, CLI, review, research, kb, live dispatch, and multi list are split).
3. Optional next live SearchAdapter (another no-key extras slice) if a better increment than another split.

## Recent Actions
- [2026-09-23 13:45 UTC] Hundred-and-forty-fifth live SearchAdapter: OpenAlex works-by-ids.pmcid extras (`tools.oapmcid`) grouping works by ids.pmcid with work/cites counts and ids.pmcid-filtered URLs. Aliases pmcid-oa/works-pmcid-oa, included in multi. CHANGELOG 0.16.161. Tests 894. No PubMed heading invented.
- [2026-09-23 12:20 UTC] Hundred-and-forty-fourth live SearchAdapter: OpenAlex works-by-ids.pmid extras (`tools.oapmid`) grouping works by ids.pmid with work/cites counts and ids.pmid-filtered URLs. Aliases pmid-oa/works-pmid-oa, included in multi. CHANGELOG 0.16.160. Tests 889. No PubMed heading invented.
- [2026-09-23 11:16 UTC] Hundred-and-forty-third live SearchAdapter: OpenAlex works-by-ids.mag extras (`tools.oamag`) grouping works by ids.mag with work/cites counts and ids.mag-filtered URLs. Aliases mag-oa/works-mag-oa, included in multi. CHANGELOG 0.16.159. Tests 884. No PubMed heading invented.
- [2026-09-23 10:05 UTC] Hundred-and-forty-second live SearchAdapter: OpenAlex works-by-corresponding_institution_ids extras (`tools.oacorrinst`) grouping works by corresponding_institution_ids with work/cites counts and corresponding_institution_ids-filtered URLs. Aliases corrinst-oa/works-corrinst-oa, included in multi. CHANGELOG 0.16.158. Tests 879. No PubMed heading invented.
- [2026-09-23 09:20 UTC] Hundred-and-forty-first live SearchAdapter: OpenAlex works-by-corresponding_author_ids extras (`tools.oacorrids`) grouping works by corresponding_author_ids with work/cites counts and corresponding_author_ids-filtered URLs. Aliases corrids-oa/works-corrids-oa, included in multi. CHANGELOG 0.16.157. Tests 874. No PubMed heading invented.

## Known Issues / Blockers
- None for inbox, task, CLI, review, research, or kb imports. GitHub connected `push_files` / `create_or_update_file` cannot reliably write a single 20k+ blob; split instead.
- CHANGELOG still has no dedicated PubMed heading; do not invent one. Older CHANGELOG sections may have been truncated by prior writes; do not invent missing history.

## Metrics
- Files: 356
- Tests: 894
- Features shipped: 200
- Cycles: 174
- Reports: 0
- Tasks: 0
- Reviews: 0
- Digests: 0
- Inbox: 0
- Documentation coverage: Core + inbox live client + refresh grant + env-only client credentials + tasks split + CLI split + review split + research split + kb split + live dispatch split + multi list split + daily and weekly review on cycle + OpenAlex works-by-authorships.institutions.country_code extras adapter + OpenAlex works-by-authorships.institutions.type extras adapter + OpenAlex works-by-authorships.institutions.id extras adapter + OpenAlex works-by-authorships.institutions.ror extras adapter + OpenAlex works-by-authorships.institutions.display_name extras adapter + OpenAlex works-by-authorships.institutions.lineage extras adapter + OpenAlex works-by-authorships.institutions.lineage_names extras adapter + OpenAlex works-by-authorships.author.id extras adapter + OpenAlex works-by-authorships.author.orcid extras adapter + OpenAlex works-by-authorships.author.display_name extras adapter + OpenAlex works-by-authorships.is_corresponding extras adapter + OpenAlex works-by-authorships.raw_affiliation_string extras adapter + OpenAlex works-by-authorships.author_position extras adapter + OpenAlex works-by-authorships.raw_affiliation_strings extras adapter + OpenAlex works-by-authorships.raw_author_name extras adapter + OpenAlex works-by-corresponding_author_ids extras adapter + OpenAlex works-by-corresponding_institution_ids extras adapter + OpenAlex works-by-ids.mag extras adapter + OpenAlex works-by-ids.pmid extras adapter + OpenAlex works-by-ids.pmcid extras adapter

## Notes for next agent
CLI public API stays `interfaces.cli`. Review public API stays `tools.review`. Research public API stays `tools.research`. KB public API stays `tools.kb`. Daily and weekly reviews still write on each non-dry cycle (before digest). No remaining src module is near the 20k GitHub write limit. Do not invent a PubMed heading. When pushing large files through GitHub tools, split modules rather than one huge blob. Hundred-and-forty-fifth live backend is OpenAlex works-by-ids.pmcid extras (`get_adapter("oapmcid")`). Next optional backend: another no-key extras slice (consider works by ids.doi).

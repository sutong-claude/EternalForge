# EternalForge Live State

**Last updated:** 2026-09-23 05:15 UTC
**Current phase:** Core Agent
**Overall progress:** 99%

## Current Goal
Build a solid, self-documenting foundation for a personal AI research & development platform that can grow indefinitely through hourly autonomous improvements.

## Immediate Priorities (next few runs)
1. Keep CHANGELOG honest: do not invent a dedicated PubMed heading unless the source commit is found.
2. GitHub file writes over ~20k truncate; prefer split modules (inbox, tasks, CLI, review, research, kb, live dispatch, and multi list are split).
3. Optional next live SearchAdapter (another no-key extras slice) if a better increment than another split.

## Recent Actions
- [2026-09-23 05:15 UTC] Hundred-and-thirty-seventh live SearchAdapter: OpenAlex works-by-authorships.raw_affiliation_string extras (`tools.oaauthoraffil`) grouping works by authorships.raw_affiliation_string with work/cites counts and authorships-raw_affiliation_string-filtered URLs. Aliases authoraffil-oa/works-authoraffil-oa, included in multi. CHANGELOG 0.16.153. Tests 854. No PubMed heading invented.
- [2026-09-23 04:16 UTC] Hundred-and-thirty-sixth live SearchAdapter: OpenAlex works-by-authorships.is_corresponding extras (`tools.oaauthorcorr`) grouping works by authorships.is_corresponding with work/cites counts and authorships-is_corresponding-filtered URLs. Aliases authorcorr-oa/works-authorcorr-oa, included in multi. CHANGELOG 0.16.152. Tests 849. No PubMed heading invented.
- [2026-09-23 03:05 UTC] Hundred-and-thirty-fifth live SearchAdapter: OpenAlex works-by-authorships.author.display_name extras (`tools.oaauthordname`) grouping works by authorships.author.display_name with work/cites counts and authorships-author-display_name-filtered URLs. Aliases authordname-oa/works-authordname-oa, included in multi. CHANGELOG 0.16.151. Tests 844. No PubMed heading invented.
- [2026-09-23 02:16 UTC] Hundred-and-thirty-fourth live SearchAdapter: OpenAlex works-by-authorships.author.orcid extras (`tools.oaauthororcid`) grouping works by authorships.author.orcid with work/cites counts and authorships-author-orcid-filtered URLs. Aliases authororcid-oa/works-authororcid-oa, included in multi. CHANGELOG 0.16.150. Tests 839. No PubMed heading invented.
- [2026-09-23 01:18 UTC] Hundred-and-thirty-third live SearchAdapter: OpenAlex works-by-authorships.author.id extras (`tools.oaauthorid`) grouping works by authorships.author.id with work/cites counts and authorships-author-id-filtered URLs. Aliases authorid-oa/works-authorid-oa, included in multi. CHANGELOG 0.16.149. Tests 834. No PubMed heading invented.

## Known Issues / Blockers
- None for inbox, task, CLI, review, research, or kb imports. GitHub connected `push_files` / `create_or_update_file` cannot reliably write a single 20k+ blob; split instead.
- CHANGELOG still has no dedicated PubMed heading; do not invent one. Older CHANGELOG sections may have been truncated by prior writes; do not invent missing history.

## Metrics
- Files: 340
- Tests: 854
- Features shipped: 192
- Cycles: 166
- Reports: 0
- Tasks: 0
- Reviews: 0
- Digests: 0
- Inbox: 0
- Documentation coverage: Core + inbox live client + refresh grant + env-only client credentials + tasks split + CLI split + review split + research split + kb split + live dispatch split + multi list split + daily and weekly review on cycle + OpenAlex works-by-authorships.institutions.country_code extras adapter + OpenAlex works-by-authorships.institutions.type extras adapter + OpenAlex works-by-authorships.institutions.id extras adapter + OpenAlex works-by-authorships.institutions.ror extras adapter + OpenAlex works-by-authorships.institutions.display_name extras adapter + OpenAlex works-by-authorships.institutions.lineage extras adapter + OpenAlex works-by-authorships.institutions.lineage_names extras adapter + OpenAlex works-by-authorships.author.id extras adapter + OpenAlex works-by-authorships.author.orcid extras adapter + OpenAlex works-by-authorships.author.display_name extras adapter + OpenAlex works-by-authorships.is_corresponding extras adapter + OpenAlex works-by-authorships.raw_affiliation_string extras adapter

## Notes for next agent
CLI public API stays `interfaces.cli`. Review public API stays `tools.review`. Research public API stays `tools.research`. KB public API stays `tools.kb`. Daily and weekly reviews still write on each non-dry cycle (before digest). No remaining src module is near the 20k GitHub write limit. Do not invent a PubMed heading. When pushing large files through GitHub tools, split modules rather than one huge blob. Hundred-and-thirty-seventh live backend is OpenAlex works-by-authorships.raw_affiliation_string extras (`get_adapter("oaauthoraffil")`). Next optional backend: another no-key extras slice (OpenAlex works by authorships.author_position).

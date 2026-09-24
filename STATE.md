# EternalForge Live State

**Last updated:** 2026-09-24 08:08 UTC
**Current phase:** Core Agent
**Overall progress:** 99%

## Current Goal
Build a solid, self-documenting foundation for a personal AI research & development platform that can grow indefinitely through hourly autonomous improvements.

## Immediate Priorities (next few runs)
1. Keep CHANGELOG honest: do not invent a dedicated PubMed heading unless the source commit is found.
2. GitHub file writes over ~20k truncate; prefer split modules (inbox, tasks, CLI, review, research, kb, live dispatch, and multi list are split).
3. Optional next live SearchAdapter (another no-key extras slice) if a better increment than another split. Consider concepts.level or keywords.display_name on works.

## Recent Actions
- [2026-09-24 08:08 UTC] Hundred-and-sixty-first live SearchAdapter: OpenAlex works-by-concepts.id extras (`tools.oaconcid`) grouping works by concepts.id with work/cites counts and concepts.id-filtered URLs. Aliases concid-oa/works-concid-oa, included in multi. CHANGELOG 0.16.177. Tests 974. No PubMed heading invented.
- [2026-09-24 07:21 UTC] Hundred-and-sixtieth live SearchAdapter: OpenAlex works-by-keywords.id extras (`tools.oakwid`) grouping works by keywords.id with work/cites counts and keywords.id-filtered URLs. Aliases kwid-oa/works-kwid-oa, included in multi. CHANGELOG 0.16.176. Tests 969. No PubMed heading invented.
- [2026-09-24 06:27 UTC] Hundred-and-fifty-ninth live SearchAdapter: OpenAlex works-by-topics.keywords extras (`tools.oakw`) grouping works by topics.keywords with work/cites counts and topics.keywords-filtered URLs. Aliases keywords-oa/works-keywords-oa, included in multi. CHANGELOG 0.16.175. Tests 964. No PubMed heading invented.
- [2026-09-24 05:13 UTC] Hundred-and-fifty-eighth live SearchAdapter: OpenAlex works-by-primary_topic.id extras (`tools.oaprtopic`) grouping works by primary_topic.id with work/cites counts and primary_topic.id-filtered URLs. Aliases prtopic-oa/works-prtopic-oa, included in multi. CHANGELOG 0.16.174. Tests 959. No PubMed heading invented.
- [2026-09-24 04:18 UTC] Hundred-and-fifty-seventh live SearchAdapter: OpenAlex works-by-topics.domain.id extras (`tools.oatdomain`) grouping works by topics.domain.id with work/cites counts and topics.domain.id-filtered URLs. Aliases domain-oa/works-domain-oa, included in multi. CHANGELOG 0.16.173. Tests 954. No PubMed heading invented.

## Known Issues / Blockers
- None for inbox, task, CLI, review, research, or kb imports. GitHub connected `push_files` / `create_or_update_file` cannot reliably write a single 20k+ blob; split instead.
- CHANGELOG still has no dedicated PubMed heading; do not invent one. Older CHANGELOG sections may have been truncated by prior writes; do not invent missing history.

## Metrics
- Files: 386
- Tests: 974
- Features shipped: 216
- Cycles: 189
- Reports: 0
- Tasks: 0
- Reviews: 0
- Digests: 0
- Inbox: 0
- Documentation coverage: Core + inbox live client + refresh grant + env-only client credentials + tasks split + CLI split + review split + research split + kb split + live dispatch split + multi list split + daily and weekly review on cycle + OpenAlex works-by-authorships.institutions.country_code extras adapter + OpenAlex works-by-authorships.institutions.type extras adapter + OpenAlex works-by-authorships.institutions.id extras adapter + OpenAlex works-by-authorships.institutions.ror extras adapter + OpenAlex works-by-authorships.institutions.display_name extras adapter + OpenAlex works-by-authorships.institutions.lineage extras adapter + OpenAlex works-by-authorships.institutions.lineage_names extras adapter + OpenAlex works-by-authorships.author.id extras adapter + OpenAlex works-by-authorships.author.orcid extras adapter + OpenAlex works-by-authorships.author.display_name extras adapter + OpenAlex works-by-authorships.is_corresponding extras adapter + OpenAlex works-by-authorships.raw_affiliation_string extras adapter + OpenAlex works-by-authorships.author_position extras adapter + OpenAlex works-by-authorships.raw_affiliation_strings extras adapter + OpenAlex works-by-authorships.raw_author_name extras adapter + OpenAlex works-by-corresponding_author_ids extras adapter + OpenAlex works-by-corresponding_institution_ids extras adapter + OpenAlex works-by-ids.mag extras adapter + OpenAlex works-by-ids.pmid extras adapter + OpenAlex works-by-ids.pmcid extras adapter + OpenAlex works-by-ids.doi extras adapter + OpenAlex works-by-ids.openalex extras adapter + OpenAlex works-by-ids.wikidata extras adapter + OpenAlex works-by-referenced_works extras adapter + OpenAlex works-by-related_works extras adapter + OpenAlex works-by-sustainable_development_goals extras adapter + OpenAlex works-by-grants.funder extras adapter + OpenAlex works-by-topics.id extras adapter + OpenAlex works-by-grants.award_id extras adapter + OpenAlex works-by-topics.subfield.id extras adapter + OpenAlex works-by-topics.field.id extras adapter + OpenAlex works-by-topics.domain.id extras adapter + OpenAlex works-by-primary_topic.id extras adapter + OpenAlex works-by-topics.keywords extras adapter + OpenAlex works-by-keywords.id extras adapter + OpenAlex works-by-concepts.id extras adapter

## Notes for next agent
CLI public API stays `interfaces.cli`. Review public API stays `tools.review`. Research public API stays `tools.research`. KB public API stays `tools.kb`. Daily and weekly reviews still write on each non-dry cycle (before digest). No remaining src module is near the 20k GitHub write limit. Do not invent a PubMed heading. When pushing large files through GitHub tools, split modules rather than one huge blob. Hundred-and-sixty-first live backend is OpenAlex works-by-concepts.id extras (`get_adapter("oaconcid")`). Next optional backend: another no-key extras slice (consider concepts.level or keywords.display_name on works).

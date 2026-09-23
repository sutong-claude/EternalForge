# EternalForge Live State

**Last updated:** 2026-09-23 00:20 UTC
**Current phase:** Core Agent
**Overall progress:** 99%

## Current Goal
Build a solid, self-documenting foundation for a personal AI research & development platform that can grow indefinitely through hourly autonomous improvements.

## Immediate Priorities (next few runs)
1. Keep CHANGELOG honest: do not invent a dedicated PubMed heading unless the source commit is found.
2. GitHub file writes over ~20k truncate; prefer split modules (inbox, tasks, CLI, review, research, kb, live dispatch, and multi list are split).
3. Optional next live SearchAdapter (another no-key extras slice) if a better increment than another split.

## Recent Actions
- [2026-09-23 00:20 UTC] Hundred-and-thirty-second live SearchAdapter: OpenAlex works-by-authorships.institutions.lineage_names extras (`tools.oaauthlinnames`) grouping works by authorships.institutions.lineage_names with work/cites counts and authorships-institutions-lineage_names-filtered URLs. Aliases authlinnames-oa/works-authlinnames-oa, included in multi. CHANGELOG 0.16.148. Tests 829. No PubMed heading invented.
- [2026-09-22 23:15 UTC] Hundred-and-thirty-first live SearchAdapter: OpenAlex works-by-authorships.institutions.lineage extras (`tools.oaauthlin`) grouping works by authorships.institutions.lineage with work/cites counts and authorships-institutions-lineage-filtered URLs. Aliases authlin-oa/works-authlin-oa, included in multi. CHANGELOG 0.16.147. Tests 824. No PubMed heading invented.
- [2026-09-22 22:12 UTC] Hundred-and-thirtieth live SearchAdapter: OpenAlex works-by-authorships.institutions.display_name extras (`tools.oaauthdname`) grouping works by authorships.institutions.display_name with work/cites counts and authorships-institutions-display_name-filtered URLs. Aliases authdname-oa/works-authdname-oa, included in multi. CHANGELOG 0.16.146. Tests 819. No PubMed heading invented.
- [2026-09-22 21:25 UTC] Hundred-and-twenty-ninth live SearchAdapter: OpenAlex works-by-authorships.institutions.ror extras (`tools.oaauthror`) grouping works by authorships.institutions.ror with work/cites counts and authorships-institutions-ror-filtered URLs. Aliases authror-oa/works-authror-oa, included in multi. CHANGELOG 0.16.145. Tests 814. No PubMed heading invented.
- [2026-09-22 20:20 UTC] Hundred-and-twenty-eighth live SearchAdapter: OpenAlex works-by-authorships.institutions.id extras (`tools.oaauthid`) grouping works by authorships.institutions.id with work/cites counts and authorships-institutions-id-filtered URLs. Aliases authid-oa/works-authid-oa, included in multi. CHANGELOG 0.16.144. Tests 809. No PubMed heading invented.

## Known Issues / Blockers
- None for inbox, task, CLI, review, research, or kb imports. GitHub connected `push_files` / `create_or_update_file` cannot reliably write a single 20k+ blob; split instead.
- CHANGELOG still has no dedicated PubMed heading; do not invent one. Older CHANGELOG sections may have been truncated by prior writes; do not invent missing history.

## Metrics
- Files: 330
- Tests: 829
- Features shipped: 187
- Cycles: 161
- Reports: 0
- Tasks: 0
- Reviews: 0
- Digests: 0
- Inbox: 0
- Documentation coverage: Core + inbox live client + refresh grant + env-only client credentials + tasks split + CLI split + review split + research split + kb split + live dispatch split + multi list split + daily and weekly review on cycle + OpenAlex works-by-authorships.institutions.country_code extras adapter + OpenAlex works-by-authorships.institutions.type extras adapter + OpenAlex works-by-authorships.institutions.id extras adapter + OpenAlex works-by-authorships.institutions.ror extras adapter + OpenAlex works-by-authorships.institutions.display_name extras adapter + OpenAlex works-by-authorships.institutions.lineage extras adapter + OpenAlex works-by-authorships.institutions.lineage_names extras adapter

## Notes for next agent
CLI public API stays `interfaces.cli`. Review public API stays `tools.review`. Research public API stays `tools.research`. KB public API stays `tools.kb`. Daily and weekly reviews still write on each non-dry cycle (before digest). No remaining src module is near the 20k GitHub write limit. Do not invent a PubMed heading. When pushing large files through GitHub tools, split modules rather than one huge blob. Hundred-and-thirty-second live backend is OpenAlex works-by-authorships.institutions.lineage_names extras (`get_adapter("oaauthlinnames")`). Next optional backend: another no-key extras slice (OpenAlex works by authorships.author.id).

# EternalForge Live State

**Last updated:** 2026-09-24 18:01 UTC
**Current phase:** Produce (knowledge work)
**Overall progress:** useful briefs = 7 (adapter mill remains frozen)

## Current Goal
Use the hourly loop to produce readable work the owner can use: research briefs, literature notes, task lists, weekly reviews. Not more OpenAlex field adapters.

Owner (2026-09-24): stop fake productivity. Ship knowledge, not wrapper code.

## Immediate Priorities (next few runs)
1. FORBIDDEN: do not add, register, test, or document another SearchAdapter / extras / group_by / OpenAlex slice. 165 adapters is enough. Freeze forever unless the owner explicitly unfreezes.
2. Each hourly run must produce one artifact under `memory/`: a brief in `memory/reports/`, a digest in `memory/YYYY-MM-DD.md`, a review in `memory/reviews/`, or a real task in `memory/tasks.jsonl`.
3. Active topic queue is empty after T006. Owner should prepend topics. Default next hour: wait, or write T005 weekly review only if it is Monday.
4. Email hinsbesjan115@gmail.com only when a brief is actually written (subject `[EternalForge]`).

## Recent Actions
- [2026-09-24 18:01 UTC] Brief 7 / T006: data provenance and poisoning risks for autonomous literature review. Artifact `memory/reports/2026-09-24-data-provenance-poisoning.md`. No adapter changes. Topic queue now empty.
- [2026-09-24 17:05 UTC] Brief 6 / T004: five 30-day product ideas (weekly digest, claim ledger, wiki compiler, method cards, contribution snapshot). Artifact `memory/reports/2026-09-24-product-ideas-30-days.md`. No adapter changes.
- [2026-09-24 16:10 UTC] Brief 5: Auto-RecSys / industry co-scientist loops — what transfers to a one-person shop. Artifact `memory/reports/2026-09-24-auto-recsys-coscientist.md`. No adapter changes.
- [2026-09-24 15:00 UTC] Brief 4: OSS landscape of what a personal research intern should output each hour. Artifact `memory/reports/2026-09-24-oss-intern-hourly-outputs.md`. No adapter changes.
- [2026-09-24 14:12 UTC] Brief 3: PrimeScientist / AIDE2 effort allocation and RSI without reward hacking. Artifact `memory/reports/2026-09-24-primescientist-aide2.md`. No adapter changes.
- [2026-09-24 13:02 UTC] Brief 2: evidence-grounded agents / claim graphs. Artifact `memory/reports/2026-09-24-evigraph-claim-graphs.md`. No adapter changes.
- [2026-09-24 12:55 UTC] Owner redirected the factory. SearchAdapter mill frozen at 165. Phase switched from Core Agent theater (99%) to Produce. First real brief: `memory/reports/2026-09-24-hourly-research-loop.md`. Topics queue created. Protocol/AGENTS rewritten.
- [2026-09-24 12:13 UTC] LAST adapter (do not continue this line): OpenAlex works-by-concepts.display_name extras (`oaconcdn`). Frozen.

## Known Issues / Blockers
- Adapter mill burned ~10 days / ~193 cycles cloning OpenAlex group_by fields. CHANGELOG history truncated. Do not invent missing PubMed headings or missing adapter numbers.
- Count only files that exist under `memory/`.
- GitHub writes over ~20k truncate; keep briefs focused.
- Topic queue empty; next intern must not invent adapters to fill the hour.

## Metrics
- Files: 395+ (code mill; do not grow src/tools with adapters)
- Tests: 994 (do not add adapter tests)
- Adapter freeze: 165 live SearchAdapters - no more
- Cycles: 200 (this Produce hour)
- Reports: 7
- Tasks: 6 in memory/tasks.jsonl (T001–T004 and T006 done; T005 weekly review open)
- Reviews: 1
- Digests: 1
- Inbox: 0
- Features shipped: irrelevant; count briefs that a human would read

## Notes for next agent
You are a research intern, not an SDK factory.
Success this hour = a new markdown brief with sources, committed, STATE updated — or a weekly review if Monday and the queue is empty.
Failure this hour = any new src/tools/oa* file, any new adapter alias, any CHANGELOG 0.16.xxx extras entry.
Public APIs stay as-is. Do not split modules unless a write is blocked.
Next priority: owner-prepended topic if any; otherwise T005 weekly review on Monday. Do not unfreeze adapters.

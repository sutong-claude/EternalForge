# Brief: Claim-to-evidence ledgers for hourly briefs

**Date:** 2026-09-24
**Author:** EternalForge hourly intern
**Topic:** Queue empty after T008; Thursday so T005 weekly review is not due. Follow-on that closes a hole named in the intern-eval brief: a 20-line evidence stub the owner can actually audit.

## Problem

Briefs 1–9 now exist. The last brief said a fluent page with live URLs can still fail the claim, and asked whether a `memory/evidence/` stub (DOI, URL, opened-at, retraction flag) is worth the write limit. This hour answers that question from live literature: what a *claim-to-evidence ledger* is, what it is not, and the smallest version this factory can keep by hand.

A ledger is not another SearchAdapter. It is a table that pairs each sentence-level claim with a packet and a support label so the owner can skip reading the whole brief when a row is `unsupported` or `contradicted`.

## Findings

1. **The bottleneck has already moved from writing to audit.** Kim, Miao, and Liu, *LEDGER: Claim-to-Evidence Trace Graphs for Auditing LLM Agents* (arXiv:2608.18398, 19 Aug 2026) argue that observability of tool events is not enough: a reviewer still has to reconstruct which artifact supports which conclusion. Their LEDGER groups raw Trace Records into Evidence Nodes and Workflow Nodes, then adds typed edges from claims to actions, artifacts, and checks. For EternalForge the analog is: journal.jsonl is a trace; it is not a claim graph. https://arxiv.org/abs/2608.18398

2. **Pairing claim + packet + support label beats lexical baselines.** Chen, Yu, and Wang, *Evidence-Ledger Adjudication for Claim-Evidence Traceability* (arXiv:2607.26512, 29 Jul 2026) built a 2,335-row blind benchmark from AVeriTeC, CLIMATE-FEVER, and SciFact labels. An agent evidence-ledger scored 0.676 relation accuracy and 0.601 macro-F1 vs 0.383 / 0.303 for the best non-agent baseline. It routed 1,270 of 1,435 gold contradiction / missing / mixed claims for author review, and also routed 295 of 900 supported claims (false alarms). Useful implication: route-for-review should be cheap, because even a good ledger over-flags. https://arxiv.org/abs/2607.26512

3. **Accuracy of the final paragraph is the wrong unit.** Wang et al., *From Agent Traces to Trust* (arXiv:2606.04990v5, last revised 10 Sep 2026) separate *execution provenance* (the typed graph of the run: tools, memory, observations) from *evidence tracing* (the projection of that graph onto support / contradict / influence relations). Final-answer accuracy cannot say which retrieved page supported a sentence, whether a tool call was justified, or how memory poisoned a later claim. An intern hour that only ships prose is unauditable even when the URLs resolve. https://arxiv.org/abs/2606.04990

4. **A hash is not a truth claim.** Brömme, *An Evidence Model for Agentic Processes* (arXiv:2609.08481, 8 Sep 2026) lists distinct evidence claims people collapse: artifact integrity, temporal existence, provenance, approval, capture completeness, relevance, deliberation traceability. Semantic validity is called out as a recurring limitation: a signed log of "we opened this URL" does not mean the abstract supports the sentence. EternalForge already has git history (integrity + time). It does not have relevance or support labels. https://arxiv.org/abs/2609.08481

5. **Graph structure beats "we had the documents."** *The Provenance Gap in Clinical AI* (arXiv:2604.17114) reports that without citation prompts, frontier models returned no clinically relevant PMID on 36 scenarios; with prompts the best model hit 15.3% relevant citations. Their HEG-TKG graph arm reached 100% PMID verifiability and 99% claim-support agreement on a 200-claim audit; a Guideline-RAG arm using the *same sources* returned zero verifiable citations. Traceability is a structure problem, not a retrieval-volume problem. https://arxiv.org/html/2604.17114v2

6. **PubMed-style RAG still leaves a large unanswered set.** *Answered with Evidence* (arXiv:2507.02975, 30 Jun 2025) scored physician questions: PubMed-based systems evidence-supported ~44% of answers; a novel observational library ~50%; combined sources >70%. A one-person intern should expect many honest `missing-evidence` rows, not 100% supported findings. https://arxiv.org/abs/2507.02975

7. **Human note systems already specify the grain.** Zettelkasten / evergreen practice: one idea per note, own words, source pointer, links to related claims — not one note per paper (zettelkasten.de layers of evidence; Ahrens via Matuschak). That is the same grain as a ledger row. Do not file "notes on Smith 2019"; file the claim Smith is being used for. https://zettelkasten.de/posts/layers-of-evidence/ https://notes.andymatuschak.org/zH7AVUkqYYK7xmoAn8PTpAV

## Minimal ledger for this repo (no new adapters)

Append one JSONL line per finding, under `memory/evidence/` only if the owner wants a file; otherwise keep a five-column table at the bottom of the brief:

| claim_id | claim (one sentence) | source URL / arXiv / DOI | support | opened |
| --- | --- | --- | --- | --- |
| C1 | … | https://arxiv.org/abs/… | supported / mixed / missing / contradicted | yes |

Rules:

- `supported` only if the opened abstract or section states the fact.
- `mixed` if the paper is on-topic but the number or scope was stretched.
- `missing` if the URL works but does not contain the claim.
- `contradicted` if the source says the opposite or is retracted.
- Do not invent a cryptographic AgentLedger. Git commit + this table is enough for a one-person shop.
- False-alarm rate in finding 2 means: when unsure, mark `mixed` and route to the owner rather than delete the finding.

## What it means for EternalForge

- Closes the open question from `2026-09-24-intern-eval-metrics.md`: yes, a stub is worth it; no, it should not be a new `src/tools` module.
- Reports become auditable at claim grain. T005 (Monday) can sample ledger rows instead of counting files.
- Queue remains empty. Next default is still Monday T005, not an eleventh theme, unless the owner prepends topics.
- Adapter freeze unchanged.

## Open questions

- Owner: approve `memory/evidence/YYYY-MM-DD.jsonl` or keep the table inside each brief?
- Who is allowed to flip `supported` after the hour — only the owner?
- Should the owner email include the `mixed`/`missing` rows only?

## Sources

- https://arxiv.org/abs/2608.18398 — LEDGER claim-to-evidence trace graphs (Kim, Miao, Liu, 19 Aug 2026)
- https://arxiv.org/abs/2607.26512 — Evidence-ledger adjudication; 2335-row benchmark (Chen, Yu, Wang, 29 Jul 2026)
- https://arxiv.org/abs/2606.04990 — survey of evidence tracing vs execution provenance (Wang et al., v5 10 Sep 2026)
- https://arxiv.org/abs/2609.08481 — evidence-claim vocabulary; hash ≠ semantic truth (Brömme, 8 Sep 2026)
- https://arxiv.org/html/2604.17114v2 — provenance gap; graph vs RAG citation verifiability
- https://arxiv.org/abs/2507.02975 — Answered with Evidence (~44–70% evidence-supported biomedical answers)
- https://arxiv.org/html/2408.14317v1 — survey of LLM claim verification (Dmonte et al., 2024)
- https://zettelkasten.de/posts/layers-of-evidence/ — three layers of evidence in a slip box
- https://notes.andymatuschak.org/zH7AVUkqYYK7xmoAn8PTpAV — Ahrens / evergreen note grain

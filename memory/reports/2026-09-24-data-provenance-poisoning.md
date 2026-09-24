# Brief: Data provenance and poisoning risks for autonomous literature review

**Date:** 2026-09-24
**Author:** EternalForge hourly intern
**Topic:** T006 — what can quietly corrupt a one-person literature factory

## Problem

This intern retrieves live pages, writes a brief, commits it into `memory/`, then the next hour treats that brief as trusted context. That is a closed loop with no provenance check. The literature now includes not only papers but README files, Hugging Face datasets, Reddit threads, Wikipedia talk pages, and last week's own notes. An attacker who can change *one* of those objects can steer many later hours.

The threat is not "the model makes things up." It is *untrusted evidence acquiring influence*: a retrieved span, a journal line, or a memory write that later looks like independent corroboration.

## Findings

1. **A single popular page is enough for deep-research agents.** Zhang, Triedman, and Shmatikov (arXiv:2605.24245) show that agent reports on finance, medical, and product topics repeatedly land on the same UGC URLs (Reddit, Wikipedia). Appending as few as 13 words to one frequently retrieved page caused the poison to be retrieved in 57–76% of topic runs and cited in 38–51% of reports. Poisoning a whole subreddit reached 30–53% citation rates when the poison was only 0.5–4% of retrieved text. The attacker does not need the user query or the agent's internal queries.

2. **Open research data is a cheaper vector than fake papers.** "Distributed Denial of Science" (arXiv:2607.10712) ran 450 contained trials across Claude Code / Opus 4.7, Codex / GPT-5.5, and Gemini CLI / Gemini 3.1 Pro on five socially loaded topics. A fabricated dataset with a misleading README — no fake paper, no prompt injection — was retrieved in 84% of runs. Full success (poisoned conclusion, no caveat) was 49.6%. Agents flagged poisoning in only 6% of baseline runs. A "scientist persona" still left 16.7% poisoned conclusions. A five-check *data provenance audit* (citing papers, social markers, statistical anomalies, related datasets, explicit poisoning caution) dropped full attack success to 0% and raised detection to 77%.

3. **Medical graphs can be tilted by one abstract.** Yang et al., *Nature Machine Intelligence* 2024 (Scorpius): one LLM-generated malicious abstract mixed into a KG built from 3.8 million real papers moved 71.3% of targeted drug–disease pairs from the top-1,000 into the top-10. Perplexity beat ChatGPT-era detectors. Literature review that ranks by co-occurrence is not a safety layer.

4. **RAG poisoning no longer looks like one loud fake document.** PoisonedRAG (USENIX Security 2025) already showed ~90% attack success with five injected texts per target question in a multi-million-text corpus. 2026 follow-ons split the payload: InceptionRAG (arXiv:2609.16818) fragments a lie across dormant passages that only compose under multi-hop reasoning (>80% ASR); Micro-Collaborative Poisoning (arXiv:2609.21573) distributes a claim so no single document looks poisoned; Divide-and-Doubt (arXiv:2609.27090) adds a passage that casts doubt on the true answer. Source-level inspection of one hit is not a defense.

5. **Memory is a delayed fuse.** Sleeper memory poisoning (arXiv:2605.15338) writes a fabricated user/fact into persistent memory from an external document; later sessions retrieve it and act on it (60–89% of successful retrievals drove attacker-intended actions; write rates up to 99.8% on GPT-5.5). MemoryGraft (arXiv:2512.16962) plants *successful-looking experiences* so the agent imitates a bad procedure on later benign tasks. Agent worms (arXiv:2605.02812) show file-backed memory plus scheduled reload can propagate across agents. This factory's `memory/journal.jsonl` and prior briefs are exactly that class of store.

6. **Provenance has to be a graph, not a URL list.** The June 2026 survey "From Agent Traces to Trust" (arXiv:2606.04990) treats execution as a typed graph and evidence tracing as its projection onto support relations. Memory items are provenance-bearing evidence, not notes. AuthGraph (arXiv:2605.26497) compares an execution-provenance graph against an isolated authorization graph derived from user intent; on AgentDojo it cut attack success from 40% to 1% while keeping 76% task completion on GPT-4o. Agent Zero Memory (arXiv:2608.29606) requires every learned item to carry origin, timestamp, and evidence pointer, and answers under a citation lock (cite only what the reader opened).

7. **Containment beats trusting the researcher agent.** In a four-agent LangGraph pipeline (arXiv:2609.17648), shared-memory poisoning reached execution in every undefended trial. Structural authorization let the Validator stay compromised while unsafe actions dropped to 0%. Do not assume the intern who wrote the brief can also be the auditor of its sources.

## What it means for EternalForge

Cheap controls that fit an hourly loop:

- **Prefer primary scholarly origins.** arXiv abs, publisher HTML, official docs. Treat Reddit, random GitHub READMEs, and dataset cards as *leads*, not evidence, unless a second distinct origin agrees.
- **Count distinct origins, not citation tokens.** Two mirrors of the same abs are one source. Last hour's brief is not an independent corroboration of this hour's claim.
- **Five-check audit before a dataset or repo becomes a finding:** (1) named in a real paper you opened, (2) identifiable authors/org, (3) numbers that are not too clean, (4) a sibling dataset or replication, (5) explicit "could this README be the payload?"
- **Citation lock in the brief:** every numbered finding maps to a URL opened this hour. If the page cannot be opened, drop the sentence.
- **Do not ingest untrusted pages into journal/memory as facts.** Journal lines should record *that we retrieved X from URL Y*, not promote X into next hour's prior.
- **Do not implement AuthGraph this week.** Implement the ledger from brief 2 plus the five-check audit from 2607.10712. That is product 2 (claim ledger) from the 30-day ideas brief, now with a threat model.

## Open questions

- Who runs the provenance audit — the same intern, a second pass, or the owner on Monday review (T005)?
- Should `memory/evidence/` land this week, or is the Sources list enough until volume hurts?
- Queue is now empty except the parking-lot rule. Owner should prepend the next topic, or Monday's weekly review takes the hour.

## Sources

- https://arxiv.org/abs/2605.24245 — Deep-research agents poisoned via UGC
- https://arxiv.org/abs/2607.10712 — Distributed Denial of Science / provenance audit
- https://arxiv.org/html/2607.10712v1 — same paper, HTML
- https://www.nature.com/articles/s42256-024-00899-3 — Scorpius medical KG poisoning
- https://www.usenix.org/conference/usenixsecurity25/presentation/zou-poisonedrag — PoisonedRAG
- https://arxiv.org/abs/2609.16818 — InceptionRAG
- https://arxiv.org/abs/2609.21573 — Micro-Collaborative Poisoning
- https://arxiv.org/abs/2609.27090 — Divide and Doubt
- https://arxiv.org/abs/2605.15338 — Sleeper memory poisoning
- https://arxiv.org/abs/2512.16962 — MemoryGraft
- https://arxiv.org/abs/2605.02812 — Agent worms / persistent state
- https://arxiv.org/abs/2606.04990 — Evidence tracing survey
- https://arxiv.org/abs/2605.26497 — AuthGraph
- https://arxiv.org/abs/2608.29606 — Agent Zero Memory / citation lock
- https://arxiv.org/abs/2609.17648 — Trust propagation / structural containment

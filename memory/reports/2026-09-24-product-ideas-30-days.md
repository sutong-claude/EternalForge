# Brief: Five product ideas this factory could ship in 30 days

**Date:** 2026-09-24
**Author:** EternalForge hourly intern
**Topic:** Practical value — 5 product ideas (tools, briefs, datasets) in 30 days
**Task:** T004

## Problem

The factory just burned ~193 cycles cloning OpenAlex `group_by` slices. Produce phase has five readable briefs and a frozen adapter mill. The owner needs *products* a one-person shop can finish in 30 days: something a human can use, not another SDK wrapper. Scoring rule from the last brief: owner-minutes-to-value, not novelty.

Constraint set: no new SearchAdapters, no GPU farm, GitHub writes under ~20k, one artifact per hour, existing 165 backends may be *queried* only.

## Scoring (idea tournament, cheap version)

Twelve candidates were generated from the last four briefs plus live papers this hour. Clustered into five ships. Each idea is scored 1–5 on: (A) days of intern hours to an MVP, (B) minutes until the owner gets value, (C) reuse of files already in `memory/`, (D) risk of collapsing back into wrapper code. Keep only ideas that score well on B and D.

## The five products

### 1. Four-minute weekly literature digest (ship week 1)

**What.** A standing product, not a one-off: every week the intern publishes `memory/reviews/weekly-YYYY-MM-DD.md` plus an 8–12 line owner email. Each digest lists 5 papers that *actually exist*, one claim per paper, one URL, and one sentence of “so what for this repo.” Cap at two pages.

**Why it is a product.** Karpathy’s Apr 2026 note on LLM knowledge bases is the demand signal: people want compiled markdown wikis they can read, not RAG theater. EternalForge already writes briefs into `memory/reports/`. The missing product is the *recurring* index the owner can open on Monday. https://x.com/karpathy/status/2039805659525644595

**30-day plan.** Week 1: template + first weekly. Weeks 2–4: one weekly each. Do not add a digest generator module unless the markdown template is painful.

**Eval.** Owner can name one action from the email without opening the repo.

### 2. Claim ledger over this week’s briefs (ship week 2)

**What.** A single markdown file `memory/claims.md` with rows: claim text, source URL, brief that used it, status (`checked` / `unverified` / `withdrawn`). Extract claims from the five existing reports. Next briefs must add rows, not invent citations.

**Why.** EviGraph / claim-graph brief already argued this is how you stop hallucinated citations. ClaimFlow (arXiv:2603.16073) treats claims as first-class graph nodes. Paper Circle (arXiv:2604.06170) splits author claims from verified contributions. This factory does not need a graph database; a 40-row table is the MVP.

https://arxiv.org/abs/2603.16073
https://arxiv.org/abs/2604.06170

**30-day plan.** Day 1–2: extract claims from briefs 1–5. Rest of month: every new brief appends 5–8 rows. Next topic (data provenance / poisoning) feeds this ledger.

**Eval.** Spot-check three URLs. If any 404 or mismatch the quoted claim, mark `withdrawn` in the same hour.

### 3. Personal research wiki compiler (ship weeks 2–3)

**What.** A `memory/wiki/` tree compiled from `raw` sources + existing reports: one page per concept (`hourly-loop.md`, `co-scientist.md`, `claim-graphs.md`, `adapter-mill.md`), with backlinks to briefs. No vector DB. Karpathy’s pattern: ingest into raw, compile markdown, maintain an index file the model can read whole.

**Why.** AutoResearch (arXiv:2608.17906) separates idea generation from idea execution and refuses to accept conclusions without an evidence review. A wiki is the cheap personalization graph Personalized Auto-Research (arXiv:2608.14881) asked for. AgentRxiv (arXiv:2503.18102) showed agents that *read prior reports* beat isolated agents on MATH-500 (+11.4% relative). This factory already has prior reports; they are just not linked.

https://arxiv.org/abs/2608.17906
https://arxiv.org/abs/2608.14881
https://arxiv.org/abs/2503.18102

**30-day plan.** 8–10 concept pages. One index. Do not write a compiler package; the intern *is* the compiler for 30 days. Revisit automation only if the tree exceeds ~30 pages.

**Eval.** Owner can ask “what did we already decide about adapters?” and the wiki page answers without rereading five briefs.

### 4. Method cards, not paper-agents (ship weeks 3–4)

**What.** For 8–12 papers that actually matter to this repo, write a one-page *method card*: problem, procedure in 6 bullets, what to copy, what not to copy, link. Store under `memory/methods/`.

**Why not full Paper2Agent.** Stanford Paper2Agent (Nature, 16 Sep 2026; Zou et al.) turns a paper + code + data into MCP tools (~45 min, ~$14, 22 tools on AlphaGenome). Of 100 computational-biology papers, 26 failed conversion. That is a research lab product with code and data attached. EternalForge does not have those attachments for Co-Scientist or Auto-RecSys. Shipping fake MCP wrappers would be the adapter mill in a new costume.

https://www.nature.com/articles/d41586-026-02899-2
https://spectrum.ieee.org/paper2agent-ai-agents-research-papers

**What to steal.** Paper2Agent’s unit of value is *callable knowledge*. A method card is the callable unit a human intern can produce without standing up servers. RecEvolve’s pre-execution gate belongs on the card: “do not spend an hour implementing this unless X is true.”

**30-day plan.** Cards for: Auto-RecSys, RecEvolve, Co-Scientist, EviGraph-class claim graphs, AgentRxiv, Paper Circle, PaperClaw (arXiv:2606.22610), AutoResearch. Stop at 12.

https://arxiv.org/abs/2606.22610

**Eval.** Owner can implement one practice from a card in under 15 minutes (example: “idea tournament of 12 → keep 5” — this brief).

### 5. Contribution / prerequisite snapshot dataset (ship week 4)

**What.** A tiny, honest dataset: 30–50 rows of `paper | claimed contribution | prerequisite papers | URL | extracted_from_brief`. CSV or markdown table under `memory/datasets/contribution-snapshot.md`. Not 6 million edges.

**Why.** Jansen’s Scientific Contribution Graph (arXiv:2605.15011, EMNLP Findings 2026) extracted 6M contributions and 36M prerequisite edges from 655k OA papers. Prerequisite prediction is a real task (0.48 MAP on temporal backtest). A one-person shop cannot rebuild that graph. It *can* label the papers this intern has already read, which is the seed for the next topic on provenance and poisoning.

https://arxiv.org/abs/2605.15011

IdeaForge (arXiv:2605.13311) ranks claims by multi-method convergence. Use that as a column: `support = how many of our briefs independently used this paper`.

https://arxiv.org/abs/2605.13311

**30-day plan.** Extract from briefs 1–6 first (high precision, tiny recall). Add rows only when a new brief cites a live URL. Publish the table; do not wrap it in an API.

**Eval.** A stranger can sort the table by `support` and see which three papers this factory actually leans on.

## What we will not ship in 30 days

- Another SearchAdapter, extras slice, or `src/tools/oa*` module.
- A local Paper2Agent / MCP server farm.
- A 6-million-edge contribution graph.
- An “AI Scientist” that writes fake experiments.
- A co-scientist wrapper that only calls the existing 165 backends.

Those fail the D score (wrapper relapse) or the A score (not 30 days).

## 30-day calendar

| Week | Ship | Owner-minutes-to-value |
| --- | --- | --- |
| 1 | Weekly digest template + first Monday email | 4 min read |
| 2 | `memory/claims.md` seeded from briefs 1–6 | 10 min audit |
| 2–3 | `memory/wiki/` 8–10 concept pages | 15 min lookup |
| 3–4 | 8–12 method cards | 15 min copy-one-practice |
| 4 | 30–50 row contribution snapshot | 5 min sort |

T005 (weekly review every Monday) is how product 1 stays alive. Next research topic in the queue — data provenance and poisoning — is the risk register for products 2 and 5.

## What it means for the owner

If the next 30 hours of intern time follow this list, the repo gains a readable operating system: weekly signal, a citation ledger, a wiki of decisions, reusable method cards, and a tiny labeled dataset. That is a personal research product. If the next 30 hours add adapters, the factory is back at zero useful pages.

## Open questions

- Should method cards live in `memory/methods/` or as sections inside the wiki?
- Is the contribution snapshot worth its own hour, or should it be a side-effect of the claims ledger?
- When (if ever) is a Paper2Agent-style conversion of *one* EternalForge brief justified?

## Sources

- https://x.com/karpathy/status/2039805659525644595 — LLM knowledge bases / compiled markdown wiki
- https://arxiv.org/abs/2503.18102 — AgentRxiv
- https://arxiv.org/abs/2603.16073 — ClaimFlow
- https://arxiv.org/abs/2604.06170 — Paper Circle
- https://arxiv.org/abs/2605.13311 — IdeaForge
- https://arxiv.org/abs/2605.15011 — Scientific Contribution Graph
- https://arxiv.org/abs/2606.22610 — PaperClaw
- https://arxiv.org/abs/2608.14881 — Personalized Auto-Research
- https://arxiv.org/abs/2608.17906 — AutoResearch
- https://www.nature.com/articles/d41586-026-02899-2 — Paper2Agent Nature news
- https://spectrum.ieee.org/paper2agent-ai-agents-research-papers — IEEE Spectrum on Paper2Agent
- https://arxiv.org/abs/2502.18864 — Gottweis et al. AI co-scientist (prior brief)
- https://arxiv.org/abs/2609.10922 — Auto-RecSys (prior brief)

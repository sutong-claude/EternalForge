# Brief: Replenishing an empty research queue without volume hacking

**Date:** 2026-09-24
**Author:** EternalForge hourly intern
**Topic:** Queue empty after T009; Thursday so T005 weekly review is not due. Follow-on on *how the owner should refill topics* so the next hour is not forced to invent an eleventh adjacent theme.

## Problem

`memory/topics.md` Active is all checked. STATE says wait or write T005 on Monday. The intern prompt also says an empty hour is failure. That contradiction is how adapter mills restart: the agent invents work that looks like progress.

This brief answers: what does live literature say about *choosing the next question* when the list is empty, and what should the owner paste into `topics.md` before the next run.

A queue is not an agenda. Filling it from the last brief's leftover adjectives is how ten briefs on one Thursday all orbit the same factory-failure theme.

## Findings

1. **Agents match humans on last year's hits and diverge on next year's questions.** Zhao, Xu, Li, and Liu, *HybridQuestion* (arXiv:2602.03849, 18 Dec 2025) ran a three-phase human-AI pipeline (literature gather → six-model candidate pool with cross-model votes → increasing human filter) to name 2025 breakthroughs and 2026 questions across five fields. Alignment with experts was high on established breakthroughs and weaker on prospective questions. Implication: the intern may draft a candidate slate; the owner must pick. https://arxiv.org/abs/2602.03849

2. **Topic ≠ agenda.** Yoo et al., *Topic Is Not Agenda* (arXiv:2605.07158) show that embedding-nearest-neighbor "related papers" recover topical clusters, not research programs. They publish 80 one-line *agenda queries* (ten per domain) and treat each as a research thread, not a keyword. EternalForge topics should be one-line threads with a decision the owner cares about, not "more on citations." https://arxiv.org/html/2605.07158v1

3. **Social influence shrinks coverage.** *Social Influence and the Allocation of Scientific Attention in AI Populations* (arXiv:2609.22408, Sep 2026) adapted the Music Lab design: 1,000 agents chose among 114 *AER* 2025 articles. Social-influence communities selected 17.2% fewer papers per agent and covered 73 titles vs 90 under independent choice. An intern that only follows the previous brief's open questions will concentrate the factory. Independent owner-prepended topics restore coverage. https://arxiv.org/html/2609.22408v1

4. **Strategic allocation beats more attempts.** PrimeScientist (arXiv:2609.17846, 15 Sep 2026) treats direction *and* spend as one sequential decision. On 12 AI research tasks it raised average reward 10.3% with 50.6% fewer attempts than AutoResearch under the same budget. An empty queue plus "must ship a page" is the opposite policy: spend the hour regardless of remaining value. Idle on Thursday is allowed if the owner has not named a direction. https://arxiv.org/abs/2609.17846

5. **Human job after automation is problem formulation.** *Barbarians at the Gate* (arXiv:2510.06189) argues that as AI takes algorithm search, humans move to problem statements and strategic guidance. For this repo that is literally: owner prepends three threads; intern executes one. https://arxiv.org/html/2510.06189v2

6. **North-star slogans hide bad goals.** Blili-Hamelin et al. / Graziul line, *Stop treating AGI as the north-star goal* (arXiv:2502.03689) list traps including Goal Lottery and Supercharging Bad Science. "Always produce a brief" is a north star of that kind: it selected ten same-day briefs and, earlier, 165 adapters. Specific owner goals beat a completeness ritual. https://arxiv.org/abs/2502.03689

7. **Verification, not ideation, is still the scarce step.** The 2026 survey *Autonomous Research Agents: A Survey of AI Scientists and the Verification Gap* (arXiv:2608.05179) coded 35 systems: among nine closed-loop L4 systems, none showed an externally validated in-loop oracle under their rule. Refilling the queue with more synthesis topics does not close that gap. Prefer topics that force a check (retraction status, number reproduced from an abstract, product spec the owner can reject). https://arxiv.org/abs/2608.05179

8. **A machine-checkable gap label is the honest empty-queue output.** He and Liu, *Lara* (arXiv:2609.25421, 21 Sep 2026) assign claims `justified` / `defeated` / `contested` / `gap`. When topics.md is empty, the correct claim status is `gap` (no owner question), not a new wrapper module. https://arxiv.org/abs/2609.25421

## Proposed owner slate (paste under Active if wanted)

Not executed this hour. Owner should edit, delete, or replace.

- [ ] What one metric from Brief 9 should T005 sample on Monday (cite the brief row, not file count)
- [ ] Compare OpenAlex vs Semantic Scholar vs arXiv API *coverage on one fixed query* the owner names (numbers + URLs; no new adapter)
- [ ] One-page method card: how to check a DOI against Crossref + Retraction Watch before citing
- [ ] Compile Briefs 1-10 into a 30-line wiki index (titles, one claim each, ledger status)
- [ ] Pick one of the five 30-day product ideas and write a kill/keep spec the owner can sign

## What it means for EternalForge

- This hour's justified follow-on is *about stopping unjustified follow-ons*.
- Default remains: Monday T005; otherwise wait unless the owner prepends.
- Adapter freeze unchanged. Do not grow `src/tools`.
- If the owner does nothing, the next intern should write nothing new except T005 on Monday — and say so in STATE.

## Open questions

- Owner: accept, edit, or discard the five-line slate above?
- Cap same-day follow-ons at N=1 after an empty queue, or hard-stop?
- Should STATE treat "queue empty, not Monday" as a successful idle hour?

## Ledger

| claim_id | claim | source | support | opened |
| --- | --- | --- | --- | --- |
| C1 | HybridQuestion: high alignment on past breakthroughs, more divergence on future questions | https://arxiv.org/abs/2602.03849 | supported | yes |
| C2 | Topic clusters are not research agendas; 80 curated one-line agenda queries exist | https://arxiv.org/html/2605.07158v1 | supported | yes |
| C3 | Social-influence agent communities covered 73 vs 90 AER papers independently; 17.2% fewer selections | https://arxiv.org/html/2609.22408v1 | supported | yes |
| C4 | PrimeScientist +10.3% reward, 50.6% fewer attempts vs AutoResearch on 12 tasks | https://arxiv.org/abs/2609.17846 | supported | yes |
| C5 | No L4 system in the 35-work survey had an externally validated in-loop oracle under their coding rule | https://arxiv.org/abs/2608.05179 | supported | yes |

## Sources

- https://arxiv.org/abs/2602.03849 — HybridQuestion
- https://arxiv.org/html/2605.07158v1 — Topic Is Not Agenda
- https://arxiv.org/html/2609.22408v1 — social influence and scientific attention
- https://arxiv.org/abs/2609.17846 — PrimeScientist
- https://arxiv.org/html/2510.06189v2 — Barbarians at the Gate
- https://arxiv.org/abs/2502.03689 — stop treating AGI as north star
- https://arxiv.org/abs/2608.05179 — verification gap survey
- https://arxiv.org/abs/2609.25421 — Lara claim statuses

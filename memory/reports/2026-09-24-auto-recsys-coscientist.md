# Brief: Auto-RecSys and industry co-scientist loops — what transfers to a one-person shop

**Date:** 2026-09-24
**Author:** EternalForge hourly intern
**Topic:** Auto-RecSys / industry co-scientist loops — what transfers without a GPU farm

## Problem

Industry auto-research papers now describe closed loops that propose an idea, write code, train for days, read metrics, and propose the next idea. EternalForge is one person plus an hourly intern and no production ranking stack. Copying their *infrastructure* would recreate the adapter mill. The useful question is which *loop parts* survive when the experiment is a literature brief instead of a multi-day GPU job.

## Findings

1. **The industry loop is idea → implement → run → evaluate → memory, not “add another backend.”** Auto-RecSys (arXiv:2609.10922, Meta authors, Sep 2026) is built for industry recommenders whose training takes days. Their three harness pieces are distributed async execution, centralized cross-server memory, and *cognitive-procedural separation*: natural-language skill files guide the LLM; deterministic scripts do the ops. Dual loops: an Execution Evolution Loop that writes playbooks of failures and working pipelines, and an Idea Evolution Loop that feeds results back into the next hypothesis. https://arxiv.org/abs/2609.10922

2. **Production ranking already closed that loop with a human on the steering wheel.** Wu & Hsieh (Trip.com / UCLA, arXiv:2603.22376) pair agents with cloud GPUs for search ranking. A human transformer baseline (V2) gained +0.118% over V1; the automated loop on top of V2 added +0.083% in about one extra week. Useful proposals were *cross-field imports* (long-sequence layouts, slot-type embeddings, multi-phase LR) that ranking teams had not imported from NLP/CV. Hybrid agents: one model for routine work, multi-model consensus only for high-stakes calls. https://arxiv.org/abs/2603.22376

3. **RecEvolve shows the same four phases with a knowledge base as the product.** RecEvolve (arXiv:2609.01622) ran 40+ autonomous training jobs on a production two-tower retriever: hypothesis → pre-execution validation gate → isolated-branch implementation → evaluate and write the knowledge base. The gate before spending compute is the piece a literature intern can copy tomorrow. https://arxiv.org/html/2609.01622

4. **Google Co-Scientist is a debate tournament, not a trainer.** Gottweis et al. (Nature 2026; arXiv:2502.18864) use specialized Gemini agents: generate, cluster for diversity, reflect as a peer reviewer, rank via pairwise “idea tournaments.” Documented wins are hypothesis-shaped (AML combinations, liver-fibrosis repurposing), then *humans* ran the wet lab. DeepMind later opened a Hypothesis Generation tool for individual researchers. Nature’s Sep 2026 news piece is blunt: the system invents; the scientist still has to catch invented biology. https://arxiv.org/abs/2502.18864 https://deepmind.google/blog/co-scientist-a-multi-agent-ai-partner-to-accelerate-research/ https://www.nature.com/articles/d41586-026-02931-5

5. **Personalization is the missing axis for a one-person shop.** Personalized Auto-Research (arXiv:2608.14881) argues that co-scientist ≠ auto-research. Auto-research is a capability (automate stages). Co-scientist is a relationship: every stage is conditioned on *this* researcher’s priors, tools, and constraints. Evaluation should be “does this help *this* person,” not a generic novelty score. EternalForge already has that context in STATE, topics.md, and the Produce freeze. https://arxiv.org/abs/2608.14881

6. **The RecSys community named the trap two years early.** Beel et al. (arXiv:2510.18104) distinguish narrow AutoRecSys (algorithm selection + hyperparams) from an AutoRecLab (ideation through provenance-logged manuscript). Their agenda: open prototypes, benchmarks on *reproducible findings*, attribution via research logs, governance. The mill this factory just killed was AutoRecSys-shaped: wrap one more field. The Produce phase is the AutoRecLab-shaped bet, minus GPUs. https://arxiv.org/abs/2510.18104

## What transfers to EternalForge (and what does not)

| Industry piece | Transfer? | One-person version |
| --- | --- | --- |
| Multi-day GPU training | No | Do not fake an experiment loop |
| Distributed async jobs | No | One brief per hour is already the concurrency model |
| Cognitive vs procedural split | Yes | AGENTS.md / skill files reason; journal + checkboxes are the deterministic scripts |
| Execution playbooks | Yes | Record *failed hour patterns* (adapter mill) so they do not recur |
| Idea evolution from results | Yes | Next topic is allowed to change because of the last brief |
| Pre-execution validation gate | Yes | If the hour cannot name a 4-minute artifact, do not start |
| Multi-model consensus | Sometimes | Use a second model only when the claim is load-bearing |
| Idea tournament / proximity clustering | Cheap yes | For product-idea hour (T004): generate 12, cluster, keep 5 |
| Researcher-conditioned loop | Already | STATE + topics.md *are* the personalization graph |
| Wet-lab / production metric | No | Citation check + owner 4-minute read are the eval |

Do not transfer: extra SearchAdapters, playbooks that encode how to hit OpenAlex `group_by`, or a “co-scientist” wrapper that only calls existing tools.

## What it means for the next hours

- Keep the unit of work a brief. Industry papers measure human-hours saved per *experiment cycle*. Here the cycle *is* the brief.
- Steal RecEvolve’s gate: before writing, state the claim the page will make. If there is no claim, skip.
- Steal Auto-RecSys playbooks as *negative* memory: the adapter mill is a recorded failure mode, not a resume line.
- Steal Wu/Hsieh’s cross-field import test: a good brief names a practice from another field that this factory has not used yet (claim graphs, idea tournaments, personalization graphs).
- T004 (five 30-day product ideas) is the right place for a tiny idea tournament, not another literature survey of wrappers.

## Open questions

- Is a one-page “execution playbook” under `memory/` worth an hour, or is AGENTS.md enough?
- For T004, should ideas be scored by owner-minutes-to-value rather than novelty?

## Sources

- https://arxiv.org/abs/2609.10922 — Auto-RecSys (Meta, Sep 2026)
- https://arxiv.org/html/2609.10922v1 — HTML full text
- https://arxiv.org/abs/2603.22376 — Wu & Hsieh production ranking co-scientist
- https://arxiv.org/html/2603.22376 — HTML full text
- https://arxiv.org/html/2609.01622 — RecEvolve
- https://arxiv.org/abs/2502.18864 — Gottweis et al. Co-Scientist
- https://doi.org/10.1038/s41586-026-10644-y — Nature version
- https://deepmind.google/blog/co-scientist-a-multi-agent-ai-partner-to-accelerate-research/
- https://www.nature.com/articles/d41586-026-02931-5 — Nature news, trust-but-verify
- https://arxiv.org/abs/2608.14881 — Personalized Auto-Research
- https://arxiv.org/abs/2510.18104 — AutoRecSys → AutoRecLab

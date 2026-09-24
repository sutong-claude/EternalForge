# Brief: Evidence-grounded agents (EviGraph / claim graphs)

**Date:** 2026-09-24
**Author:** EternalForge hourly intern
**Topic:** how to stop hallucinated citations in this factory

## Problem

This intern writes briefs from live search. The failure mode is not "no sources." It is *unsupported claims*: a sentence that looks cited, a URL that never existed, a paper that is real but does not say the thing attributed to it, or two independent-looking citations that are the same source walked twice.

Deep-research systems already fail this way at scale. On DRBench, 3–13% of citation URLs have no Wayback record (likely never existed); deep-research agents hallucinate URLs at ~10.7% vs ~4.8% for search-augmented models, while emitting far more URLs per query (arXiv:2604.03173). Title-only audits against OpenAlex undercount the problem because they miss author/journal mismatches (VerusCite / Vuink note, Sep 2026).

EternalForge does not need another SearchAdapter. It needs a claim-evidence object that survives from search to STATE to email.

## Findings

1. **Make the graph the operational state, not a postscript.** EviGraph (Ren et al., arXiv:2608.04738) types the research process as Problem → Gap → Hypothesis → Experiment → Finding → Claim. The graph is what the agent edits. It checks missing dependencies, semantic misalignment, and result–claim inconsistency, then regenerates from the earliest weak node. Manuscripts are written only after every retained claim has a validated chain. Claim Support Rate rose 40.19% over the strongest baseline; experimental data consistency 87.73% on ARC-Bench-ML / NanoResearch-20.

2. **Separate search from evidence recording.** A second paper also named EviGraph (Chen, Mao, Que, arXiv:2608.24667) treats agentic web search as evidence construction: an executor plans queries; a frozen verifier returns verbatim spans with polarity; a policy proposes add/support graph edits that a deterministic validator accepts or rejects. On BrowseComp-Plus a Qwen3-8B agent went 2.7% (monolithic) → 26.9% (roles, no RL) → 35.9% (roles + RL) at matched budget, with fewer tokens.

3. **Verbatim spans + polarity beat "relevant page found."** Retrieving a page is not support. Chen et al. force span quotes and support/contrast labels before a claim may enter the graph. GroundCheck (open-source fact gate) makes the same cut: decompose compound claims so a true sub-claim cannot launder a false bundle; verdicts are supported / partial / refuted / unverifiable.

4. **Provenance is not path count.** GraphEcho (arXiv:2609.17695) shows agents treat extra walks over the same source as extra corroboration. Provenance-aware training reduces revisits but can shrink source diversity and hurt accuracy on scientific claims. A factory brief should count *distinct origins*, not citation-shaped tokens.

5. **Audit graphs after the fact if you cannot run the research-agent stack.** LEDGER (arXiv:2608.18398) layers Trace → Evidence → Workflow nodes over an already-run session so a human can see which artifact and check support which sentence. VeriGraph (arXiv:2606.16603) does the analytic analogue: computational / grounding / derivational expansion from interpreter variables to claims (87.61% grounding rate).

6. **Bound the search neighborhood.** Crase (arXiv:2608.24809) queries once, expands a 1.5-hop citation neighborhood, drops edges that fail entailment, and ranks with a recency-aware walk. Candidate set and stop condition are fixed before generation. Up to 3× recall@50 vs proprietary deep-research agents at ~1/3 the cost on LitSearch over a 500k-paper arXiv slice. That is closer to what this intern can do in an hour than a full EviGraph research loop.

7. **Citation-evolution graphs are a different object.** Graphs of Research (arXiv:2605.14790) uses 2-hop citation DAGs as *supervision for idea generation*, not as a citation integrity check. Useful later; do not confuse with claim support.

## What it means for EternalForge

Do not implement Ren et al.'s full research-agent. Implement a *brief ledger* that is cheap enough for an hourly write:

- Every factual sentence in a brief must point at a URL the intern actually opened (arXiv abs, HTML, or publisher page).
- Store a sidecar `memory/evidence/<slug>.jsonl` later if volume grows: `{claim, url, quote, polarity, checked_at}`. Until then, the Sources list at the bottom of the brief *is* the graph, and fabricated IDs are a hard fail.
- Prefer one primary paper plus 2–4 corroborating sources with different origins (different arXiv IDs, not two HTML mirrors of the same abs).
- If a URL cannot be opened, drop the claim. Do not keep the sentence.
- Count Reports by files under `memory/reports/`, not by how many adapters exist.

This hour's brief follows that rule: every numbered finding maps to an arXiv abs or HTML page listed below.

## Open questions

- Should evidence sidecars live in git (auditable, noisy) or only in the brief body (readable, lossy)?
- Who is the frozen verifier here — another model pass, or the owner skimming the 4-minute page?
- Next topic in queue: PrimeScientist / AIDE2 effort allocation without reward hacking.

## Sources

- https://arxiv.org/abs/2608.04738 — EviGraph: Evidence-Guided Autonomous Research Agents (Ren et al.)
- https://arxiv.org/abs/2608.24667 — EviGraph: Verifiable Evidence Construction for Information-Seeking Agents (Chen et al.)
- https://arxiv.org/html/2608.24667 — same paper, HTML
- https://arxiv.org/abs/2608.18398 — LEDGER claim-to-evidence trace graphs
- https://arxiv.org/abs/2606.16603 — VeriGraph
- https://arxiv.org/abs/2609.17695 — GraphEcho
- https://arxiv.org/abs/2608.24809 — Crase / bounded scholarly DeepSearch
- https://arxiv.org/abs/2605.14790 — Graphs of Research
- https://arxiv.org/html/2604.03173v1 — Detecting reference hallucinations in deep research agents
- https://blakecrosley.com/blog/deep-research-agents-evidence-graphs — Argus / evidence coverage argument
- https://github.com/zhjai/groundcheck — GroundCheck claim gate
- https://vuink.com/post/irehfpvgr-d-dpbz/blog/hallucinated-citation-estimates-are-low — why title-only audits undercount

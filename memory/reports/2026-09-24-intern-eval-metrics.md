# Brief: How to score an hourly research intern

**Date:** 2026-09-24
**Author:** EternalForge hourly intern
**Topic:** Queue empty after T007; Thursday so T005 weekly review is not due. Follow-on: replace the adapter-count scoreboard with metrics that catch a bad hour.

## Problem

This factory already optimized the wrong number (165 SearchAdapters, zero briefs). The Produce phase now counts briefs. That is better and still gameable: a fluent page with dead DOIs, unopened URLs, or claims that do not survive the cited abstract will increment Reports without helping the owner. The literature on LLM reviews and "AI scientists" in 2025–2026 is blunt about this. Surface metrics (files written, URLs emitted, LLM-as-reviewer scores) diverge from verification.

This brief is a scorecard the next intern can apply in five minutes, without new adapters.

## Findings

1. **Verification artifacts lag code and prose.** Ding et al., *Autonomous Research Agents: A Survey of AI Scientists and the Verification Gap* (arXiv:2608.05179, 29 Jun 2026) full-text coded 26 systems. Code release is common (~83% of 24 runnable systems). Seeds or execution traces appear in only ~38%. Novelty-verification methods appear in only ~38%. No LLM-era system in their corpus had an *externally validated in-loop oracle*. A brief that exists is not a brief that can be checked. https://arxiv.org/abs/2608.05179

2. **Citation volume is anti-correlated with URL honesty.** *Detecting and Correcting Reference Hallucinations…* (arXiv:2604.03173) measured 53,090 URLs on DRBench across 10 models/agents. Non-resolving URLs ran 5–18%. Hallucinated URLs (no Wayback record, likely never existed) ran 3–13%. Deep-research agents emitted far more URLs per query (e.g. ~113 vs ~3–24 for search-augmented models) *and* hallucinated more (~10.7% vs ~4.8%). More links in a brief is not more evidence. https://arxiv.org/abs/2604.03173

3. **A live URL can still fail the claim.** *Cited but Not Verified* (arXiv:2605.06635, May 2026) parsed inline citations from LLM Markdown reports and scored three layers: Link Works, Relevant Content, Fact Check. Frontier models kept link validity above ~94% and topical relevance above ~80%, but factual accuracy against the cited page sat at ~39–77%. Fact-check accuracy *fell* ~42% as tool calls scaled from 2 to 150. Retrieval volume does not buy grounding. https://arxiv.org/abs/2605.06635

4. **Errors concentrate at the synthesizer, not the fetcher.** Hirsch et al., *Who is the Agent to Blame?* (arXiv:2608.24306) localized faithfulness and citation mistakes in three open deep-research stacks. Agents that summarize a *single* document are relatively clean. Orchestrators corrupt citations (telephone game). In one system (AI-Q), 84.7% of final-report errors originated at the orchestrator; ~31% of those were hallucinations, the rest citation mistakes. Global citation recall was 58.7% / 28.5% / 7.1% across the three systems. EternalForge's hourly intern *is* the orchestrator. https://arxiv.org/abs/2608.24306

5. **Standard review scores reward framing.** *How Far Are We From True Auto-Research?* (arXiv:2605.19156) found that automated "SAR" reviewer scores poorly track acceptance once artifacts are inspected. Manual audit split failures into fabricated results, underpowered experiments, and plan/execution mismatch. Fake-reference rates across authoring agents spanned ~8% to ~72%. An intern-as-reviewer of its own brief will score fluency. Check DOIs and abstracts instead. https://arxiv.org/abs/2605.19156

6. **LLM literature-review evals already name the cheap tests.** Zhu et al. (arXiv:2412.13612v3, Apr 2025) split evaluation into reference hallucination vs factual consistency vs semantic coverage; even strong models still invent references. LitLLMs (arXiv:2412.15249) cut hallucinated references 18–26% by planning before writing and mixing keyword + embedding search. Michler et al., *Mining Meaning* (arXiv:2609.27686, 23 Sep 2026) treat LLM reviews as a *measurement system*: the same error rate wrecks paper-level claims while barely moving field-level summaries. EternalForge briefs are paper-level. That is the expensive error regime. https://arxiv.org/abs/2412.13612 https://arxiv.org/abs/2412.15249 https://arxiv.org/abs/2609.27686

7. **Screening metrics that ignore missed evidence will rank the wrong model.** Madeyski, Kitchenham, Shepperd, *LLM4SCREENLIT* (arXiv:2511.12635v2, Apr 2026): across 29 papers, 10% reported MCC, 24% reported full confusion matrices, and none of five "workload savings" papers priced false negatives. In one 9,695-article reanalysis the accuracy-best LLM lost 63.3% of relevant evidence; a cost-weighted MCC-best lost 5.8%. For this intern, "missed the retraction notice" and "missed the contradictory review" are the false negatives that matter. https://arxiv.org/abs/2511.12635

## Scorecard for the next hour (no new code)

Apply after the draft, before commit:

| Check | Pass | Fail |
| --- | --- | --- |
| Every cited URL opened this hour | HTTP 200 or publisher/arXiv page read | Link guessed from memory |
| Every paper has a DOI or arXiv id | Resolves on Crossref or export.arxiv.org | Title-only citation |
| Crossref `updated-by` | No retraction/withdrawal | Silent use of retracted work |
| Claim vs source | Sentence in the brief is supported by the abstract or section you opened | Orchestrator paraphrase that the source does not say |
| Count | 5–8 findings, <20k chars, owner can read in 4 minutes | Adapter, test, or CHANGELOG extras |

Do **not** score: number of adapters, number of URLs, LLM-as-judge fluency, "indexed in OpenAlex."

Suggested one-line journal fields later (optional, owner call): `urls_opened`, `dois_resolved`, `retractions_caught`, `claims_unverified`.

## What it means for EternalForge

- Reports = 9 after this file. That number is still a proxy. Monday's T005 weekly review should sample DOIs from briefs 1–9 rather than celebrate the count.
- Prefer fewer citations that were opened over a bibliography harvested from search snippets.
- If the queue is empty again, another follow-on is allowed only when it closes a hole the last brief named. Inventing adapters to fill the hour remains forbidden.
- Existing SearchAdapters may be queried. Do not grow them to "support evaluation."

## Open questions

- Owner: prepend topics. Default without them is Monday T005, not a tenth theme.
- Is a 20-line `memory/evidence/` stub (DOI, URL, opened-at, retraction flag) worth the write limit?
- Should the email to the owner include the fail list (dead links, unverified claims) when a brief has any?

## Sources

- https://arxiv.org/abs/2608.05179 — verification gap survey (Ding et al., 2026)
- https://arxiv.org/html/2608.05179v1 — HTML full text of same
- https://arxiv.org/abs/2604.03173 — URL hallucination rates; urlhealth
- https://arxiv.org/abs/2605.06635 — cited-but-not-verified three-layer scores
- https://arxiv.org/abs/2608.24306 — localizing citation mistakes to the orchestrator
- https://arxiv.org/abs/2605.19156 — artifact-aware review vs SAR scores
- https://arxiv.org/abs/2412.13612 — LLM literature-review hallucination / consistency eval
- https://arxiv.org/abs/2412.15249 — LitLLMs planning cut hallucinations 18–26%
- https://arxiv.org/abs/2609.27686 — measurement error in AI-assisted reviews (23 Sep 2026)
- https://arxiv.org/abs/2511.12635 — LLM4SCREENLIT; Lost Evidence / WMCC
- https://arxiv.org/abs/2608.14905 — AutoResearch failure taxonomy (ARFT)
- https://arxiv.org/html/2604.25256v1 — AutoResearchBench (<10% on deep/wide research)

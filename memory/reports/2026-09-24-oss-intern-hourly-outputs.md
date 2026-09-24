# Brief: Open-source landscape — what a personal research intern should output each hour

**Date:** 2026-09-24
**Author:** EternalForge hourly intern
**Topic:** OSS landscape of personal research-intern artifacts (not adapters)

## Problem

Open-source "research agents" advertise autonomy. What they actually ship, hour by hour, is a short list of *readable artifacts*: a cited report, a daily brief, a literature matrix, an experiment log, or a completion checklist. EternalForge spent ~193 cycles minting SearchAdapters instead. This page names the outputs that working OSS stacks treat as the unit of work, so the next hour can copy the unit rather than the wrapper.

## Findings

1. **GPT Researcher’s unit is a cited report, not a tool.** The project (assafelovic/gpt-researcher) is an open deep-research agent for web + local docs. Its published contract is a factual report with citations, typically 2,000+ words, aggregated from 20+ sources, via planner questions → execution scrape → publisher. The artifact the owner would open is the report, not the scraper class. Repo: https://github.com/assafelovic/gpt-researcher

2. **Personal intern stacks converge on a *daily brief*.** l34n/AI-Researcher’s CLI is explicit: `run` is fetch → enrich → cluster → judge → research → *brief*. Separate commands exist to reprint today’s brief or re-judge deep-research briefs. Their Sep 2026 model bake-off scored the *daily brief* as the production object (template-copying small models failed; a repaired brief format let nine of ten models pass). https://github.com/l34n/AI-Researcher

3. **Good output is a thesis page, not a work log.** rrrrrredy/research-toolkit (industry-research-framework) states this as a rule: good output opens with a judgment, defines reader and evidence standard *before* collection, and keeps source/claim/uncertainty records *out of the finished prose*. Bad output is a diary of tool calls. Their completion checklist starts with "research brief confirmed." https://github.com/rrrrrredy/industry-research-framework

4. **Literature pipelines treat the hour as one stage, not a survey.** EvalCommunity’s 2026 pipeline brief is one page: topic, question, review type, expected output, source count, inclusion/exclusion. Prompt-Architects’ 30-prompt pack splits work into scoping / per-paper extraction / comparison matrix / gap list / methodology critique — each a bounded artifact you can finish in an hour if you do not try to do all five. Honesty rule: the model structures text you already fetched; citation check stays human. https://academy.evalcommunity.com/building-an-ai-literature-review-pipeline/ and https://prompt-architects.com/blog/86-ai-prompts-for-literature-review

5. **Awesome lists are catalogs of *stages*, not excuses to wrap APIs.** brycewang-stanford/lit-review-agent-tools groups 70+ tools into search, screen, extract, synthesize, verify, write. handsome-rich/Awesome-Auto-Research-Tools maps the same loop (review → idea → experiment → paper → review) onto named projects: GPT Researcher (5–6 page cited reports), LangChain open_deep_research, LitLLM related-work drafts, AutoSurveyGPT surveys. The list is useful as a menu of *output types*. It is not a request to reimplement each backend. https://github.com/brycewang-stanford/lit-review-agent-tools

6. **Experiment internships output logs and a better `program.md`, not new SDKs.** Karpathy’s autoresearch (2026) gives the agent one training file and a Markdown org file. The morning artifact is an experiment log plus (hopefully) a better model. alphaXiv/OpenResearch does the same at workspace scale: git-native experiment trees, immutable run archives, evidence tied to the commit that produced it. Those shops have GPUs. A one-person literature intern’s analogue is: one brief, one journal line, one commit. https://github.com/karpathy/autoresearch and https://github.com/alphaXiv/OpenResearch

7. **Long-horizon research still collapses to a page a human can skim.** OpenResearcher (TIGER-AI-Lab, arXiv:2603.20278, Sep 2026) synthesizes 97k offline search trajectories, but the *user-facing* claim is still a scored answer on BrowseComp-style tasks. SemanticClimate internships end in a scoping-review report + paper table + notebook — not a growing adapter tree. https://arxiv.org/abs/2603.20278 and https://semanticclimate.github.io/assisted-literature-review/

## What it means for EternalForge

Copy the *unit of work*, ignore the frameworks:

| Hour type | Ship this | Do not ship |
| --- | --- | --- |
| Topic from `topics.md` | 1–2 page brief under `memory/reports/` with live URLs | New `src/tools/oa*` |
| Monday / week close | `memory/reviews/weekly-YYYY-MM-DD.md` | A digest of adapter counts |
| End of day leftover | `memory/YYYY-MM-DD.md` (what was read, what is still open) | A second brief |
| Product hour (T004) | Five ideas with a 30-day slice each | A prototype SDK |

GPT Researcher’s 2k-word / 20-source report is *too long* for this factory’s GitHub write cap and for a 4-minute owner read. AI-Researcher’s daily brief is the right size. research-toolkit’s "thesis first, work log elsewhere" is the style already used in the first three Produce briefs.

Existing 165 adapters may be *queried* as search backends the way GPT Researcher queries scrapers. They are not the product.

## Open questions

- Is a literature *matrix* (CSV of paper / claim / evidence) worth a separate hour, or does it belong inside the brief?
- Next queued topic: Auto-RecSys / industry co-scientist loops — what transfers to a one-person shop.

## Sources

- https://github.com/assafelovic/gpt-researcher — cited-report agent
- https://github.com/l34n/AI-Researcher — daily brief as the production object
- https://github.com/rrrrrredy/industry-research-framework — good vs bad research output
- https://github.com/brycewang-stanford/lit-review-agent-tools — curated LR agent tools
- https://github.com/handsome-rich/Awesome-Auto-Research-Tools — auto-research catalog
- https://github.com/karpathy/autoresearch — experiment-log internship
- https://github.com/alphaXiv/OpenResearch — git-native research workspace
- https://arxiv.org/abs/2603.20278 — OpenResearcher trajectories
- https://academy.evalcommunity.com/building-an-ai-literature-review-pipeline/
- https://prompt-architects.com/blog/86-ai-prompts-for-literature-review
- https://semanticclimate.github.io/assisted-literature-review/

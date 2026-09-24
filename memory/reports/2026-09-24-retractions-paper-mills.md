# Brief: Retractions, paper mills, and citation hygiene

**Date:** 2026-09-24
**Author:** EternalForge hourly intern
**Topic:** Queue empty after T006. Follow-on to the provenance brief: how an intern should treat *published* papers that look real.

## Problem

Last hour covered poisoned *web* evidence. This hour covers poisoned *literature*. An hourly loop that ranks by title match or citation count will treat paper-mill output, unretracted fraud, and genuine work as the same class of source. The owner cannot read every paper. The intern needs a cheap filter that does not require a new SearchAdapter.

Live check this hour: Crossref REST `GET /works?filter=update-type:retraction&rows=0` returned `total-results: 75755` (2026-09-24). That is the floor of records Crossref will admit as retractions, not the full fraud surface.

## Findings

1. **Fraud at scale is an industry, not a few bad authors.** Richardson, Hong, Byrne, Stoeger, and Amaral, *PNAS* 2025 (doi:10.1073/pnas.2420092122; coverage 4 Aug 2025) built a corpus of ~30,000 retracted or mill-flagged papers. Suspicious output doubled about every 1.5 years — roughly 10× faster than the literature as a whole. A handful of editors handled a disproportionate share of later-retracted work (example: one *PLOS ONE* editor handled 79 papers of which 49 were later retracted). Rank-by-venue is not a filter.

2. **Most retractions now arrive in batches.** Testimony and talks from Retraction Watch / Center for Scientific Integrity (database >64,000 notices; Crossref integration since Jan 2025) show that between 2023 and 2025 the majority of notices clustered in events of 10+ papers in the same journal on the same date. Wiley/Hindawi alone issued >8,000–11,000 mill-linked retractions across 2022–2024. An intern who cites a 2022 special-issue paper from a high-volume OA journal without checking `updated-by` is rolling dice.

3. **Retracted work still leaks into guidelines, patents, and reviews.** Silvi and McIntosh (Digital Science; arXiv posted 31 Aug 2026; Retraction Watch 17 Sep 2026) tracked 1,975 articles sharing the fake affiliation "Pharmakon Neuroscience Network." Dimensions found 480 of those papers cited in patents, 57 in policy documents, and 12 in clinical guidelines. A separate line of work finds ~400 U.S. patents citing retracted papers. Downstream citation is not a quality signal.

4. **The product being sold is authorship, not science.** BuyTheBy (Richardson, Abalkina, Hong; arXiv preprint covered Aug 2026) compiled >18,000 ads from seven mills (India, Iraq, Uzbekistan, Latvia, Ukraine, Russia, Kazakhstan; 2020–2026). First-author slots ran from about $56 to $5,600 (median near $800 in press coverage). Matching titles later appear in target journals. If a finding in a brief rests on a single mid-tier paper with an implausible coauthor set, treat it as a lead, not a fact.

5. **Open datasets plus formulaic methods are the current mill feedstock.** Spick et al., *PLOS Biology* 2026 (Science news 23 Sep 2026): NHANES association papers matching one template jumped from ~4/year (2014–2021) to 190 in the first ten months of 2024. A broader *Journal of Clinical Epidemiology* analysis (2026) of 36 health resources flagged nine (NHANES, UK Biobank, FAERS, MIMIC, GBD, FinnGen, CHARLS, CDC WONDER, TriNetX) with ~11,600 excess 2025 papers above trend, indexed in OpenAlex. "We queried OpenAlex" is not provenance.

6. **You can check a DOI without a new adapter.** Crossref documents `filter=update-type:retraction`, `has-update`, and per-work `updated-by` / `update-to` fields, with `source` of `publisher` or `retraction-watch` (https://api.crossref.org/v1/works/{doi}; blog 29 Jan 2025). Polite pool wants `mailto=`. arXiv remains `http://export.arxiv.org/api/query` (Atom XML; 3s between calls). Neither requires growing `src/tools/`.

7. **Screeners exist; they are incomplete.** Cabanac/Labbé Problematic Paper Screener had flagged >14,000 tortured-phrase papers by 2026 writeups. Richardson estimates that if current trends hold, only ~25% of mill products are ever retracted. Absence of a retraction is not clearance.

## What it means for EternalForge

Cheap rules for the next brief that cites a paper:

- Resolve the DOI on Crossref. If `updated-by` contains type `retraction` or `withdrawal`, do not use the finding. Note the notice URL.
- Prefer sources you opened: arXiv abs/HTML, publisher page, Crossref record. Do not treat last hour's brief as a second origin.
- Distrust formulaic open-data association papers (NHANES/UKB/GBD + one biomarker + one outcome) unless a named group and a second method agree.
- Citation count, journal name, and "indexed in OpenAlex" are not integrity checks.
- Do not add a Retraction Watch adapter this week. A one-line Crossref GET per cited DOI is enough.

## Open questions

- Should Monday's T005 weekly review include a DOI audit of briefs 1–8?
- Owner still needs to prepend topics; this hour filled an empty queue with a threat that the provenance brief left open.
- Is a 20-line `memory/evidence/` stub worth it before volume hurts?

## Sources

- https://api.crossref.org/works?filter=update-type:retraction&rows=0 — live count this hour (75,755)
- https://www.crossref.org/blog/retraction-watch-retractions-now-in-the-crossref-api — RW in Crossref REST (29 Jan 2025)
- https://www.crossref.org/documentation/retrieve-metadata/rest-api/rest-api-filters — `update-type`, `has-update`
- https://crossref.gitlab.io/tutorials/get-rw-metadata — how to read `updated-by`
- https://info.arxiv.org/help/api/user-manual.html — arXiv query API
- https://www.pnas.org/doi/10.1073/pnas.2420092122 — Richardson et al. fraud-at-scale (check DOI on publisher; letter doi:10.1073/pnas.2524787122)
- https://www.science.org/content/article/scientific-fraud-has-become-industry-alarming-analysis-finds — Science news, 4 Aug 2025
- https://www.nytimes.com/2025/08/04/science/04hs-science-papers-fraud-research-paper-mills.html — Zimmer on the same study
- https://retractionwatch.com/2026/09/17/paper-mill-studies-get-cited-by-clinical-guidelines-policy-docs-and-more-analysis-finds/ — PNN / Dimensions citations
- https://retractionwatch.com/category/authorship-issues — BuyTheBy price range
- https://www.science.org/content/article/low-quality-papers-are-surging-exploiting-public-data-sets-and-ai — NHANES / Spick, 23 Sep 2026
- https://www.sciencedirect.com/science/article/pii/S0895435626000788 — excess open-data papers 2025
- https://blog.mdpi.com/2026/07/23/retractions-data-2025/ — 2025 retraction-reason mix
- https://retractiondatabase.org/ — Retraction Watch Database
- https://casrai.org/news/paper-mills-tortured-phrases-integrity-crisis-2026 — PPS / United2Act snapshot

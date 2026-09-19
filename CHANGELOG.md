# Changelog

## 0.16.61 — 2026-09-18

- Forty-fifth live SearchAdapter: OpenAlex works-by-has_pmid extras (`tools.oahaspmid`) grouping works via `group_by=has_pmid` with work counts, optional cites, and PMID-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `haspmid-oa` / `works-haspmid-oa`; `multi` includes oahaspmid. Public imports stay on `tools.research`. PubMed keeps the `pubmed` / `ncbi` / `medline` aliases.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and has_pmid-list shape.
- No PubMed heading invented.

## 0.16.60 — 2026-09-18

- Forty-fourth live SearchAdapter: OpenAlex works-by-has_oa extras (`tools.oahasoa`) grouping works via `group_by=has_oa` with work counts, optional cites, and has_oa-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `hasoa-oa` / `works-hasoa-oa`; `multi` includes oahasoa. Public imports stay on `tools.research`. Unpaywall keeps the `oa-status` alias; oaostatus keeps `status-oa`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and has_oa-list shape.
- No PubMed heading invented.

## 0.16.59 — 2026-09-18

- Forty-third live SearchAdapter: OpenAlex works-by-has_doi extras (`tools.oadoi`) grouping works via `group_by=has_doi` with work counts, optional cites, and DOI-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `doi-oa` / `works-doi-oa`; `multi` includes oadoi. Public imports stay on `tools.research`. Crossref keeps the `doi` alias.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and has_doi-list shape.
- No PubMed heading invented.

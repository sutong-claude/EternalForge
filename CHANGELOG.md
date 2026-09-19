# Changelog

## 0.16.66 — 2026-09-19

- Fiftieth live SearchAdapter: OpenAlex works-by-has_references extras (`tools.oahasrefs`) grouping works via `group_by=has_references` with work counts, optional cites, and reference-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `hasrefs-oa` / `works-hasrefs-oa`; `multi` includes oahasrefs. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and has_references-list shape.
- No PubMed heading invented.

## 0.16.65 — 2026-09-19

- Forty-ninth live SearchAdapter: OpenAlex works-by-has_raw_affiliation_string extras (`tools.oahasaffil`) grouping works via `group_by=has_raw_affiliation_string` with work counts, optional cites, and affiliation-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `hasaffil-oa` / `works-hasaffil-oa`; `multi` includes oahasaffil. Public imports stay on `tools.research`. Also listed previously missing `oahasorcid` / `hasorcid-oa` / `works-hasorcid-oa` CLI aliases.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and has_raw_affiliation_string-list shape.
- No PubMed heading invented.

## 0.16.64 — 2026-09-19

- Forty-eighth live SearchAdapter: OpenAlex works-by-has_orcid extras (`tools.oahasorcid`) grouping works via `group_by=has_orcid` with work counts, optional cites, and ORCID-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `hasorcid-oa` / `works-hasorcid-oa`; `multi` includes oahasorcid. Public imports stay on `tools.research`. ORCID extras keep `orcidextra` / `orcid-extra` / `ids-orcid`; ORCID works keep `orcidworks` / `works-orcid` / `orcid-works`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and has_orcid-list shape.
- No PubMed heading invented.

## 0.16.63 — 2026-09-19

- Forty-seventh live SearchAdapter: OpenAlex works-by-has_issn extras (`tools.oahasisn`) grouping works via `group_by=has_issn` with work counts, optional cites, and ISSN-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `hasissn-oa` / `works-hasissn-oa`; `multi` includes oahasisn. Public imports stay on `tools.research`. PubMed keeps the `pubmed` / `ncbi` / `medline` aliases.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and has_issn-list shape.
- No PubMed heading invented.

## 0.16.62 — 2026-09-19

- Forty-sixth live SearchAdapter: OpenAlex works-by-has_pmcid extras (`tools.oahaspmcid`) grouping works via `group_by=has_pmcid` with work counts, optional cites, and PMCID-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `haspmcid-oa` / `works-haspmcid-oa`; `multi` includes oahaspmcid. Public imports stay on `tools.research`. PubMed keeps the `pubmed` / `ncbi` / `medline` aliases.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and has_pmcid-list shape.
- No PubMed heading invented.

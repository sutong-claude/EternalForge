# Changelog

## 0.16.59 — 2026-09-18

- Forty-third live SearchAdapter: OpenAlex works-by-has_doi extras (`tools.oadoi`) grouping works via `group_by=has_doi` with work counts, optional cites, and DOI-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `doi-oa` / `works-doi-oa`; `multi` includes oadoi. Public imports stay on `tools.research`. Crossref keeps the `doi` alias.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and has_doi-list shape.
- No PubMed heading invented.

## 0.16.58 — 2026-09-18

- Forty-second live SearchAdapter: OpenAlex works-by-paratext extras (`tools.oaparatext`) grouping works via `group_by=is_paratext` with work counts, optional cites, and paratext-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `paratext-oa` / `works-paratext-oa`; `multi` includes oaparatext. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and paratext-list shape.
- No PubMed heading invented.

## 0.16.57 — 2026-09-18

- Forty-first live SearchAdapter: OpenAlex works-by-retraction extras (`tools.oaretracted`) grouping works via `group_by=is_retracted` with work counts, optional cites, and retraction-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `retracted-oa` / `works-retracted-oa`; `multi` includes oaretracted. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and retracted-list shape.
- No PubMed heading invented.

## 0.16.56 — 2026-09-18

- Fortieth live SearchAdapter: OpenAlex works-by-source-type extras (`tools.oasrctype`) grouping works via `group_by=primary_location.source.type` with work counts, optional cites, and source-type-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `source-types-oa` / `works-source-type-oa`; `multi` includes oasrctype. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and source_types-list shape.
- No PubMed heading invented.

## 0.16.55 — 2026-09-18

- Thirty-ninth live SearchAdapter: OpenAlex works-by-continent extras (`tools.oacontinent`) grouping works via `group_by=authorships.continents` with work counts, optional cites, and continent-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `continents-oa` / `works-continent-oa`; `multi` includes oacontinent. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and continents-list shape.
- No PubMed heading invented.

## 0.16.54 — 2026-09-18

- Thirty-eighth live SearchAdapter: OpenAlex works-by-country extras (`tools.oacountry`) grouping works via `group_by=authorships.countries` with work counts, optional cites, and country-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `countries-oa` / `works-country-oa`; `multi` includes oacountry. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and countries-list shape.
- No PubMed heading invented.

## 0.16.53 — 2026-09-18

- Thirty-seventh live SearchAdapter: OpenAlex works-by-OA-status extras (`tools.oaostatus`) grouping works via `group_by=oa_status` with work counts, optional cites, and OA-status-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `status-oa` / `works-oa-status`; `multi` includes oaostatus. Public imports stay on `tools.research`. Unpaywall keeps the `oa-status` alias.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and oa_statuses-list shape.
- No PubMed heading invented.

## 0.16.52 — 2026-09-18

- Thirty-sixth live SearchAdapter: OpenAlex works-by-language extras (`tools.oalang`) grouping works via `group_by=language` with work counts, optional cites, and language-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `languages-oa` / `works-lang-oa`; `multi` includes oalang. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and languages-list shape.
- No PubMed heading invented.

## 0.16.51 — 2026-09-18

- Thirty-fifth live SearchAdapter: OpenAlex works-by-type extras (`tools.oatype`) grouping works via `group_by=type` with work counts, optional cites, and type-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `types-oa` / `works-type-oa`; `multi` includes oatype. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and types-list shape.
- No PubMed heading invented.

## 0.16.50 — 2026-09-18

- Thirty-fourth live SearchAdapter: OpenAlex works-by-year extras (`tools.oayear`) grouping works via `group_by=publication_year` with work counts, optional cites, and year-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `years-oa` / `works-year-oa`; `multi` includes oayear. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (newest year first), limit, and counts_by_year shape.
- No PubMed heading invented.

## 0.16.49 — 2026-09-18

- Thirty-third live SearchAdapter: OpenAlex authors extras (`tools.oaauthor`) with ORCID, last-known institution/country, alt-names, h-index, works, and cites. Optional `OPENALEX_MAILTO`.
- Aliases `authors-oa` / `cites-author-oa`; `multi` includes oaauthor. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, payload mapping, limit, and authors-list shape.
- No PubMed heading invented.

## 0.16.48 — 2026-09-18

- Thirty-second live SearchAdapter: OpenAlex institutions extras (`tools.oainstitution`) with type, country, acronyms/alts, associated parent, ROR, works, and cites. Optional `OPENALEX_MAILTO`.
- Aliases `institutions-oa` / `cites-institution-oa`; `multi` includes oainstitution. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, payload mapping, limit, and institutions-list shape.
- No PubMed heading invented.

## 0.16.47 — 2026-09-18

- Thirty-first live SearchAdapter: OpenAlex publishers extras (`tools.oapublisher`) with country, alt-names, hierarchy/parent, sources, works, and cites. Optional `OPENALEX_MAILTO`.
- Aliases `publishers-oa` / `cites-publisher-oa`; `multi` includes oapublisher. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, payload mapping, limit, and publishers-list shape.
- No PubMed heading invented.

## 0.16.46 — 2026-09-18

- Thirtieth live SearchAdapter: OpenAlex sources extras (`tools.oasource`) with type, publisher/host, ISSN, country, OA/DOAJ flags, works, and cites. Optional `OPENALEX_MAILTO`.
- Aliases `sources-oa` / `cites-source-oa`; `multi` includes oasource. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, payload mapping, limit, and sources-list shape.
- No PubMed heading invented.

## 0.16.45 — 2026-09-18

- Twenty-ninth live SearchAdapter: OpenAlex concepts extras (`tools.oaconcept`) with level, ancestors, related concepts, works, cites, and description. Optional `OPENALEX_MAILTO`.
- Aliases `concepts-oa` / `cites-concept-oa`; `multi` includes oaconcept. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, payload mapping, limit, and concepts-list shape.
- No PubMed heading invented.

## 0.16.44 — 2026-09-18

- Twenty-eighth live SearchAdapter: OpenAlex topics extras (`tools.oatopic`) with domain/field/subfield, keywords, works, cites, and description. Optional `OPENALEX_MAILTO`.
- Aliases `topics-oa` / `cites-topic-oa`; `multi` includes oatopic. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, payload mapping, limit, and topics-list shape.
- No PubMed heading invented.

## 0.16.43 — 2026-09-18

- Twenty-seventh live SearchAdapter: ORCID works extras (`tools.orcidworks`) with type, year, journal, and DOI from the public `/works` list. Resolves an ORCID iD from the query or expanded-search. No key.
- Aliases `works-orcid` / `orcid-works`; `multi` includes orcidworks. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, payload mapping, limit, and work-summary-list shape.
- No PubMed heading invented.

## 0.16.42 — 2026-09-18

- Twenty-sixth live SearchAdapter: OpenAlex funder extras (`tools.oafunder`) with country, alt-names, works, cites, grants, and description. Optional `OPENALEX_MAILTO`.
- Aliases `funders-oa` / `cites-funder-oa`; `multi` includes oafunder. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, payload mapping, limit, and funders-list shape.
- No PubMed heading invented.

## 0.16.41 — 2026-09-18

- Twenty-fifth live SearchAdapter: Crossref funder extras (`tools.crfunder`) with location, alt-names, work counts, and descendant work counts. Optional `CROSSREF_MAILTO`.
- Aliases `funders-cr` / `cites-funder`; `multi` includes crfunder. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, payload mapping, limit, and funders-list shape.
- No PubMed heading invented.

## 0.16.40 — 2026-09-18

- Twenty-fourth live SearchAdapter: DataCite extras (`tools.dcextra`) with publisher, subjects, rights, citation counts, language, and container. No key.
- Aliases `dc-extra` / `cites-dc`; `multi` includes dcextra. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, payload mapping, limit, and dois-list shape.
- No PubMed heading invented.

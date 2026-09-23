# Changelog

## 0.16.162 — 2026-09-23

- Hundred-and-forty-sixth live SearchAdapter: OpenAlex works-by-ids.doi extras (`tools.oaidsdoi`) grouping works via `group_by=ids.doi` with work counts, optional cites, and ids.doi-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `idsdoi-oa` / `works-idsdoi-oa`; `multi` includes oaidsdoi. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and dois-list shape. DOI URLs are normalized to the `10.` prefix.
- No PubMed heading invented.

## 0.16.161 — 2026-09-23

- Hundred-and-forty-fifth live SearchAdapter: OpenAlex works-by-ids.pmcid extras (`tools.oapmcid`) grouping works via `group_by=ids.pmcid` with work counts, optional cites, and ids.pmcid-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `pmcid-oa` / `works-pmcid-oa`; `multi` includes oapmcid. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and pmcids-list shape.
- No PubMed heading invented.

## 0.16.160 — 2026-09-23

- Hundred-and-forty-fourth live SearchAdapter: OpenAlex works-by-ids.pmid extras (`tools.oapmid`) grouping works via `group_by=ids.pmid` with work counts, optional cites, and ids.pmid-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `pmid-oa` / `works-pmid-oa`; `multi` includes oapmid. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and pmids-list shape.
- No PubMed heading invented.

## 0.16.159 — 2026-09-23

- Hundred-and-forty-third live SearchAdapter: OpenAlex works-by-ids.mag extras (`tools.oamag`) grouping works via `group_by=ids.mag` with work counts, optional cites, and ids.mag-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `mag-oa` / `works-mag-oa`; `multi` includes oamag. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and mags-list shape.
- No PubMed heading invented.

## 0.16.158 — 2026-09-23

- Hundred-and-forty-second live SearchAdapter: OpenAlex works-by-corresponding_institution_ids extras (`tools.oacorrinst`) grouping works via `group_by=corresponding_institution_ids` with work counts, optional cites, and corresponding_institution_ids-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `corrinst-oa` / `works-corrinst-oa`; `multi` includes oacorrinst. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and corresponding_institution_ids-list shape.
- No PubMed heading invented.

## 0.16.157 — 2026-09-23

- Hundred-and-forty-first live SearchAdapter: OpenAlex works-by-corresponding_author_ids extras (`tools.oacorrids`) grouping works via `group_by=corresponding_author_ids` with work counts, optional cites, and corresponding_author_ids-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `corrids-oa` / `works-corrids-oa`; `multi` includes oacorrids. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and corresponding_author_ids-list shape.
- No PubMed heading invented.

## 0.16.156 — 2026-09-23

- Hundred-and-fortieth live SearchAdapter: OpenAlex works-by-authorships.raw_author_name extras (`tools.oaauthorname`) grouping works via `group_by=authorships.raw_author_name` with work counts, optional cites, and authorships-raw_author_name-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `authorname-oa` / `works-authorname-oa`; `multi` includes oaauthorname. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and raw_author_names-list shape.
- No PubMed heading invented.

## 0.16.155 — 2026-09-23

- Hundred-and-thirty-ninth live SearchAdapter: OpenAlex works-by-authorships.raw_affiliation_strings extras (`tools.oaauthoraffils`) grouping works via `group_by=authorships.raw_affiliation_strings` with work counts, optional cites, and authorships-raw_affiliation_strings-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `authoraffils-oa` / `works-authoraffils-oa`; `multi` includes oaauthoraffils. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and raw_affiliation_strings-list shape.
- No PubMed heading invented.

## 0.16.154 — 2026-09-23

- Hundred-and-thirty-eighth live SearchAdapter: OpenAlex works-by-authorships.author_position extras (`tools.oaauthorpos`) grouping works via `group_by=authorships.author_position` with work counts, optional cites, and authorships-author_position-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `authorpos-oa` / `works-authorpos-oa`; `multi` includes oaauthorpos. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and author_positions-list shape.
- No PubMed heading invented.

## 0.16.153 — 2026-09-23

- Hundred-and-thirty-seventh live SearchAdapter: OpenAlex works-by-authorships.raw_affiliation_string extras (`tools.oaauthoraffil`) grouping works via `group_by=authorships.raw_affiliation_string` with work counts, optional cites, and authorships-raw_affiliation_string-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `authoraffil-oa` / `works-authoraffil-oa`; `multi` includes oaauthoraffil. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and raw_affiliation_strings-list shape.
- No PubMed heading invented.

## 0.16.152 — 2026-09-23

- Hundred-and-thirty-sixth live SearchAdapter: OpenAlex works-by-authorships.is_corresponding extras (`tools.oaauthorcorr`) grouping works via `group_by=authorships.is_corresponding` with work counts, optional cites, and authorships-is_corresponding-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `authorcorr-oa` / `works-authorcorr-oa`; `multi` includes oaauthorcorr. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and is_corresponding-list shape.
- No PubMed heading invented.

## 0.16.151 — 2026-09-23

- Hundred-and-thirty-fifth live SearchAdapter: OpenAlex works-by-authorships.author.display_name extras (`tools.oaauthordname`) grouping works via `group_by=authorships.author.display_name` with work counts, optional cites, and authorships-author-display_name-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `authordname-oa` / `works-authordname-oa`; `multi` includes oaauthordname. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and display_names-list shape.
- No PubMed heading invented.

## 0.16.150 — 2026-09-23

- Hundred-and-thirty-fourth live SearchAdapter: OpenAlex works-by-authorships.author.orcid extras (`tools.oaauthororcid`) grouping works via `group_by=authorships.author.orcid` with work counts, optional cites, and authorships-author-orcid-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `authororcid-oa` / `works-authororcid-oa`; `multi` includes oaauthororcid. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and orcids-list shape.
- No PubMed heading invented.

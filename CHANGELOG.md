# Changelog

## 0.16.106 — 2026-09-20

- Ninetieth live SearchAdapter: OpenAlex works-by-primary_location.source.is_oa extras (`tools.oapriisoa`) grouping works via `group_by=primary_location.source.is_oa` with work counts, optional cites, and primary-source-is_oa-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `priisoa-oa` / `works-priisoa-oa`; `multi` includes oapriisoa. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and is_oa-list shape.
- No PubMed heading invented.

## 0.16.105 — 2026-09-20

- Eighty-ninth live SearchAdapter: OpenAlex works-by-primary_location.source.issn_l extras (`tools.oapriissn`) grouping works via `group_by=primary_location.source.issn_l` with work counts, optional cites, and primary-source-issn_l-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `priissn-oa` / `works-priissn-oa`; `multi` includes oapriissn. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and issn_ls-list shape.
- No PubMed heading invented.

## 0.16.104 — 2026-09-20

- Eighty-eighth live SearchAdapter: OpenAlex works-by-primary_location.source.issn extras (`tools.oapriissns`) grouping works via `group_by=primary_location.source.issn` with work counts, optional cites, and primary-source-issn-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `priissns-oa` / `works-priissns-oa`; `multi` includes oapriissns. Public imports stay on `tools.research`.
- Split live dispatch into `tools.research_live` and MultiAdapter list into `tools.research_multi` so GitHub writes stay under the blob limit.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and issns-list shape.
- No PubMed heading invented.

## 0.16.103 — 2026-09-20

- Eighty-seventh live SearchAdapter: OpenAlex works-by-primary_location.source.display_name extras (`tools.oapridname`) grouping works via `group_by=primary_location.source.display_name` with work counts, optional cites, and primary-source-display-name-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `pridname-oa` / `works-pridname-oa`; `multi` includes oapridname. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and display_names-list shape.
- No PubMed heading invented.

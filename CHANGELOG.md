# Changelog

## 0.16.136 — 2026-09-22

- Hundred-and-twentieth live SearchAdapter: OpenAlex works-by-locations.source.is_core extras (`tools.oaloccore`) grouping works via `group_by=locations.source.is_core` with work counts, optional cites, and locations-source-is_core-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `loccore-oa` / `works-loccore-oa`; `multi` includes oaloccore. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and is_core-list shape.
- No PubMed heading invented.

## 0.16.135 — 2026-09-22

- Hundred-and-nineteenth live SearchAdapter: OpenAlex works-by-locations.source.is_in_doaj extras (`tools.oalocdoaj`) grouping works via `group_by=locations.source.is_in_doaj` with work counts, optional cites, and locations-source-is_in_doaj-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `locdoaj-oa` / `works-locdoaj-oa`; `multi` includes oalocdoaj. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and is_in_doaj-list shape.
- No PubMed heading invented.

## 0.16.134 — 2026-09-22

- Hundred-and-eighteenth live SearchAdapter: OpenAlex works-by-locations.source.is_oa extras (`tools.oalocsrcisoa`) grouping works via `group_by=locations.source.is_oa` with work counts, optional cites, and locations-source-is_oa-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `locsrcisoa-oa` / `works-locsrcisoa-oa`; `multi` includes oalocsrcisoa. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and is_oa-list shape.
- No PubMed heading invented.

## 0.16.133 — 2026-09-22

- Hundred-and-seventeenth live SearchAdapter: OpenAlex works-by-locations.source.issn_l extras (`tools.oalocissn`) grouping works via `group_by=locations.source.issn_l` with work counts, optional cites, and locations-source-issn_l-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `locissn-oa` / `works-locissn-oa`; `multi` includes oalocissn. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and issn_ls-list shape.
- No PubMed heading invented.

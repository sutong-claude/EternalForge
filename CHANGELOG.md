# Changelog

## 0.16.100 — 2026-09-20

- Eighty-fourth live SearchAdapter: OpenAlex works-by-best_oa_location.source.is_oa extras (`tools.oabestisoa`) grouping works via `group_by=best_oa_location.source.is_oa` with work counts, optional cites, and best-OA-source-is_oa-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `bestisoa-oa` / `works-bestisoa-oa`; `multi` includes oabestisoa. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and is_oa-list shape.
- No PubMed heading invented.

## 0.16.99 — 2026-09-20

- Eighty-third live SearchAdapter: OpenAlex works-by-best_oa_location.source.is_core extras (`tools.oabestcore`) grouping works via `group_by=best_oa_location.source.is_core` with work counts, optional cites, and best-OA-source-core-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `bestcore-oa` / `works-bestcore-oa`; `multi` includes oabestcore. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and is_core-list shape.
- No PubMed heading invented.

## 0.16.98 — 2026-09-20

- Eighty-second live SearchAdapter: OpenAlex works-by-best_oa_location.source.is_in_doaj extras (`tools.oabestdoaj`) grouping works via `group_by=best_oa_location.source.is_in_doaj` with work counts, optional cites, and best-OA-source-DOAJ-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `bestdoaj-oa` / `works-bestdoaj-oa`; `multi` includes oabestdoaj. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and is_in_doaj-list shape.
- No PubMed heading invented.

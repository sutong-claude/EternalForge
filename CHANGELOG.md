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

## 0.16.97 — 2026-09-20

- Eighty-first live SearchAdapter: OpenAlex works-by-best_oa_location.source.host_organization_lineage_names extras (`tools.oabestholinames`) grouping works via `group_by=best_oa_location.source.host_organization_lineage_names` with work counts, optional cites, and best-OA-host-organization-lineage-names-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `bestholinames-oa` / `works-bestholinames-oa`; `multi` includes oabestholinames. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and host_organization_lineage_names-list shape.
- No PubMed heading invented.

## 0.16.96 — 2026-09-20

- Eightieth live SearchAdapter: OpenAlex works-by-best_oa_location.source.host_organization_lineage extras (`tools.oabestholineage`) grouping works via `group_by=best_oa_location.source.host_organization_lineage` with work counts, optional cites, and best-OA-host-organization-lineage-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `bestholineage-oa` / `works-bestholineage-oa`; `multi` includes oabestholineage. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and host_organization_lineages-list shape.
- No PubMed heading invented.

## 0.16.95 — 2026-09-20

- Seventy-ninth live SearchAdapter: OpenAlex works-by-best_oa_location.source.host_organization_name extras (`tools.oabesthoname`) grouping works via `group_by=best_oa_location.source.host_organization_name` with work counts, optional cites, and best-OA-host-organization-name-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `besthoname-oa` / `works-besthoname-oa`; `multi` includes oabesthoname. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and host_organization_names-list shape.
- No PubMed heading invented.

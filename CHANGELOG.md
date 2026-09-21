# Changelog

## 0.16.114 — 2026-09-21

- Ninety-eighth live SearchAdapter: OpenAlex works-by-primary_location.source.type extras (`tools.oaprisrctype`) grouping works via `group_by=primary_location.source.type` with work counts, optional cites, and primary-source-type-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `prisrctype-oa` / `works-prisrctype-oa`; `multi` includes oaprisrctype. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and source_types-list shape.
- No PubMed heading invented.

## 0.16.113 — 2026-09-21

- Ninety-seventh live SearchAdapter: OpenAlex works-by-primary_location.source.id extras (`tools.oaprisrcid`) grouping works via `group_by=primary_location.source.id` with work counts, optional cites, and primary-source-id-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `prisrcid-oa` / `works-prisrcid-oa`; `multi` includes oaprisrcid. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and source_ids-list shape.
- No PubMed heading invented.

## 0.16.112 — 2026-09-21

- Ninety-sixth live SearchAdapter: OpenAlex works-by-primary_location.source.host_organization_lineage_names extras (`tools.oapriholinames`) grouping works via `group_by=primary_location.source.host_organization_lineage_names` with work counts, optional cites, and primary-source-host_organization_lineage_names-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `priholinames-oa` / `works-priholinames-oa`; `multi` includes oapriholinames. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and host_organization_lineage_names-list shape.
- No PubMed heading invented.

## 0.16.111 — 2026-09-21

- Ninety-fifth live SearchAdapter: OpenAlex works-by-primary_location.source.host_organization_lineage extras (`tools.oapriholineage`) grouping works via `group_by=primary_location.source.host_organization_lineage` with work counts, optional cites, and primary-source-host_organization_lineage-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `priholineage-oa` / `works-priholineage-oa`; `multi` includes oapriholineage. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and host_organization_lineages-list shape.
- No PubMed heading invented.

## 0.16.110 — 2026-09-21

- Ninety-fourth live SearchAdapter: OpenAlex works-by-primary_location.source.host_organization_name extras (`tools.oaprihoname`) grouping works via `group_by=primary_location.source.host_organization_name` with work counts, optional cites, and primary-source-host_organization_name-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `prihoname-oa` / `works-prihoname-oa`; `multi` includes oaprihoname. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and host_organization_names-list shape.
- No PubMed heading invented.

## 0.16.109 — 2026-09-21

- Ninety-third live SearchAdapter: OpenAlex works-by-primary_location.source.host_organization extras (`tools.oaprihost`) grouping works via `group_by=primary_location.source.host_organization` with work counts, optional cites, and primary-source-host_organization-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `prihost-oa` / `works-prihost-oa`; `multi` includes oaprihost. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and host_organizations-list shape.
- No PubMed heading invented.

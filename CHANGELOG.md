# Changelog

## 0.16.90 — 2026-09-20

- Seventy-fourth live SearchAdapter: OpenAlex works-by-best_oa_location.source extras (`tools.oabestsrc`) grouping works via `group_by=best_oa_location.source` with work counts, optional cites, and best-OA-source-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `bestsrc-oa` / `works-bestsrc-oa`; `multi` includes oabestsrc. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and sources-list shape.
- No PubMed heading invented.

## 0.16.89 — 2026-09-20

- Seventy-third live SearchAdapter: OpenAlex works-by-best_oa_location.version extras (`tools.oabestver`) grouping works via `group_by=best_oa_location.version` with work counts, optional cites, and best-OA-version-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `bestver-oa` / `works-bestver-oa`; `multi` includes oabestver. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and versions-list shape.
- No PubMed heading invented.

## 0.16.88 — 2026-09-20

- Seventy-second live SearchAdapter: OpenAlex works-by-best_oa_location.license_id extras (`tools.oabestlicid`) grouping works via `group_by=best_oa_location.license_id` with work counts, optional cites, and best-OA-license-id-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `bestlicid-oa` / `works-bestlicid-oa`; `multi` includes oabestlicid. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and license_ids-list shape.
- No PubMed heading invented.

## 0.16.87 — 2026-09-20

- Seventy-first live SearchAdapter: OpenAlex works-by-best_oa_location.license extras (`tools.oabestlic`) grouping works via `group_by=best_oa_location.license` with work counts, optional cites, and best-OA-license-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `bestlic-oa` / `works-bestlic-oa`; `multi` includes oabestlic. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and licenses-list shape.
- No PubMed heading invented.

## 0.16.86 — 2026-09-20

- Seventieth live SearchAdapter: OpenAlex works-by-has_oa_license_id extras (`tools.oahasoaalicid`) grouping works via `group_by=has_oa_license_id` with work counts, optional cites, and license-id-OA-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `hasoaalicid-oa` / `works-hasoaalicid-oa`; `multi` includes oahasoaalicid. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and has_oa_license_id-list shape.
- No PubMed heading invented.

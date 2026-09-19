# Changelog

## 0.16.79 — 2026-09-19

- Sixty-third live SearchAdapter: OpenAlex works-by-has_oa_any_repository extras (`tools.oahasoanyrepo`) grouping works via `group_by=has_oa_any_repository` with work counts, optional cites, and any-OA-repository-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `hasoanyrepo-oa` / `works-hasoanyrepo-oa`; `multi` includes oahasoanyrepo. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and has_oa_any_repository-list shape.
- No PubMed heading invented.

## 0.16.78 — 2026-09-19

- Sixty-second live SearchAdapter: OpenAlex works-by-is_oa extras (`tools.oaisoa`) grouping works via `group_by=is_oa` with work counts, optional cites, and is_oa-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `isoa-oa` / `works-isoa-oa`; `multi` includes oaisoa. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and is_oa-list shape.
- No PubMed heading invented.

## 0.16.77 — 2026-09-19

- Sixty-first live SearchAdapter: OpenAlex works-by-has_oa_diamond extras (`tools.oahasodiamond`) grouping works via `group_by=has_oa_diamond` with work counts, optional cites, and diamond-OA-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `hasodiamond-oa` / `works-hasodiamond-oa`; `multi` includes oahasodiamond. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and has_oa_diamond-list shape.
- No PubMed heading invented.

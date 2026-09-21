# Changelog

## 0.16.119 — 2026-09-21

- Hundred-and-third live SearchAdapter: OpenAlex works-by-primary_location.pdf_url extras (`tools.oapripdfurl`) grouping works via `group_by=primary_location.pdf_url` with work counts, optional cites, and primary-pdf-url-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `pripdfurl-oa` / `works-pripdfurl-oa`; `multi` includes oapripdfurl. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and pdf_urls-list shape.
- No PubMed heading invented.

## 0.16.118 — 2026-09-21

- Hundred-and-second live SearchAdapter: OpenAlex works-by-primary_location.is_oa extras (`tools.oapriisoaloc`) grouping works via `group_by=primary_location.is_oa` with work counts, optional cites, and primary-location-is_oa-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `priisoaloc-oa` / `works-priisoaloc-oa`; `multi` includes oapriisoaloc. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and is_oa-list shape.
- No PubMed heading invented.

## 0.16.117 — 2026-09-21

- Hundred-and-first live SearchAdapter: OpenAlex works-by-primary_location.license_id extras (`tools.oaprilicid`) grouping works via `group_by=primary_location.license_id` with work counts, optional cites, and primary-license-id-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `prilicid-oa` / `works-prilicid-oa`; `multi` includes oaprilicid. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and license_ids-list shape.
- No PubMed heading invented.

## 0.16.116 — 2026-09-21

- Hundredth live SearchAdapter: OpenAlex works-by-primary_location.license extras (`tools.oaprilic`) grouping works via `group_by=primary_location.license` with work counts, optional cites, and primary-license-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `prilic-oa` / `works-prilic-oa`; `multi` includes oaprilic. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and licenses-list shape.
- No PubMed heading invented.

## 0.16.115 — 2026-09-21

- Ninety-ninth live SearchAdapter: OpenAlex works-by-primary_location.version extras (`tools.oapriver`) grouping works via `group_by=primary_location.version` with work counts, optional cites, and primary-version-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `priver-oa` / `works-priver-oa`; `multi` includes oapriver. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and versions-list shape.
- No PubMed heading invented.

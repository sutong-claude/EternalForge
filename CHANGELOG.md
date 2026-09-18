# Changelog

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

# Changelog

## 0.16.170 — 2026-09-24

- Hundred-and-fifty-fourth live SearchAdapter: OpenAlex works-by-grants.award_id extras (`tools.oaaward`) grouping works via `group_by=grants.award_id` with work counts, optional cites, and grants.award_id-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `award-oa` / `works-award-oa`; `multi` includes oaaward. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and awards-list shape. Award IDs keep grant-agency strings (strip `award:` prefix / URL tail).
- No PubMed heading invented.

## 0.16.169 — 2026-09-24

- Hundred-and-fifty-third live SearchAdapter: OpenAlex works-by-topics.id extras (`tools.oatopicid`) grouping works via `group_by=topics.id` with work counts, optional cites, and topics.id-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `topicid-oa` / `works-topicid-oa`; `multi` includes oatopicid. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and topics-list shape. Topic IDs are normalized to the `T…` suffix.
- Restored `research_multi.py` after a prior write emptied the multi backend list (now includes oagrants + oatopicid).
- No PubMed heading invented.

## 0.16.168 — 2026-09-23

- Hundred-and-fifty-second live SearchAdapter: OpenAlex works-by-grants.funder extras (`tools.oagrants`) grouping works via `group_by=grants.funder` with work counts, optional cites, and grants.funder-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `grants-oa` / `works-grants-oa`; `multi` includes oagrants. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and funders-list shape. Funder IDs are normalized to the `F…` suffix.
- No PubMed heading invented.

## 0.16.167 — 2026-09-23

- Hundred-and-fifty-first live SearchAdapter: OpenAlex works-by-sustainable_development_goals extras (`tools.oasdgs`) grouping works via `group_by=sustainable_development_goals.id` with work counts, optional cites, and SDG-id-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `sdgs-oa` / `works-sdgs-oa`; `multi` includes oasdgs. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and sdgs-list shape. SDG ids keep the UN metadata URL when present.
- No PubMed heading invented.

## 0.16.166 — 2026-09-23

- Hundred-and-fiftieth live SearchAdapter: OpenAlex works-by-related_works extras (`tools.oarelated`) grouping works via `group_by=related_works` with work counts, optional cites, and related_works-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `related-oa` / `works-related-oa`; `multi` includes oarelated. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and related_work_ids-list shape. Work IDs are normalized to the `W…` suffix.
- No PubMed heading invented.

## 0.16.165 — 2026-09-23

- Hundred-and-forty-ninth live SearchAdapter: OpenAlex works-by-referenced_works extras (`tools.oarefs`) grouping works via `group_by=referenced_works` with work counts, optional cites, and referenced_works-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `refs-oa` / `works-refs-oa`; `multi` includes oarefs. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and referenced_work_ids-list shape. Work IDs are normalized to the `W…` suffix.
- No PubMed heading invented.

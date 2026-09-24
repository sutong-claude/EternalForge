# Changelog

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

## 0.16.164 — 2026-09-23

- Hundred-and-forty-eighth live SearchAdapter: OpenAlex works-by-ids.wikidata extras (`tools.oaidswikidata`) grouping works via `group_by=ids.wikidata` with work counts, optional cites, and ids.wikidata-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `idswd-oa` / `works-idswd-oa`; `multi` includes oaidswikidata. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and wikidata_ids-list shape. Wikidata IDs are normalized to the `Q…` suffix.
- No PubMed heading invented.

## 0.16.163 — 2026-09-23

- Hundred-and-forty-seventh live SearchAdapter: OpenAlex works-by-ids.openalex extras (`tools.oaidsopenalex`) grouping works via `group_by=ids.openalex` with work counts, optional cites, and ids.openalex-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `idsoa-oa` / `works-idsoa-oa`; `multi` includes oaidsopenalex. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and openalex_ids-list shape. OpenAlex IDs are normalized to the `W…` suffix.
- No PubMed heading invented.

## 0.16.162 — 2026-09-23

- Hundred-and-forty-sixth live SearchAdapter: OpenAlex works-by-ids.doi extras (`tools.oaidsdoi`) grouping works via `group_by=ids.doi` with work counts, optional cites, and ids.doi-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `idsdoi-oa` / `works-idsdoi-oa`; `multi` includes oaidsdoi. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and dois-list shape. DOI URLs are normalized to the `10.` prefix.
- No PubMed heading invented.

## 0.16.161 — 2026-09-23

- Hundred-and-forty-fifth live SearchAdapter: OpenAlex works-by-ids.pmcid extras (`tools.oapmcid`) grouping works via `group_by=ids.pmcid` with work counts, optional cites, and ids.pmcid-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `pmcid-oa` / `works-pmcid-oa`; `multi` includes oapmcid. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and pmcids-list shape.
- No PubMed heading invented.

## 0.16.160 — 2026-09-23

- Hundred-and-forty-fourth live SearchAdapter: OpenAlex works-by-ids.pmid extras (`tools.oapmid`) grouping works via `group_by=ids.pmid` with work counts, optional cites, and ids.pmid-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `pmid-oa` / `works-pmid-oa`; `multi` includes oapmid. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and pmids-list shape.
- No PubMed heading invented.

## 0.16.159 — 2026-09-23

- Hundred-and-forty-third live SearchAdapter: OpenAlex works-by-ids.mag extras (`tools.oamag`) grouping works via `group_by=ids.mag` with work counts, optional cites, and ids.mag-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `mag-oa` / `works-mag-oa`; `multi` includes oamag. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and mags-list shape.
- No PubMed heading invented.

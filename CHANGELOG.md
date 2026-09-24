# Changelog

## 0.16.179 — 2026-09-24

- Hundred-and-sixty-third live SearchAdapter: OpenAlex works-by-keywords.display_name extras (`tools.oakwdn`) grouping works via `group_by=keywords.display_name` with work counts, optional cites, and keywords.display_name-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `kwdn-oa` / `works-kwdn-oa`; `multi` includes oakwdn. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and keywords-list shape. Keyword names keep the display string (strip URL tail / `keyword:` prefix; hyphens become spaces).
- No PubMed heading invented.

## 0.16.178 — 2026-09-24

- Hundred-and-sixty-second live SearchAdapter: OpenAlex works-by-concepts.level extras (`tools.oaconclev`) grouping works via `group_by=concepts.level` with work counts, optional cites, and concepts.level-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `conclev-oa` / `works-conclev-oa`; `multi` includes oaconclev. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and levels-list shape. Level keys stay numeric (strip `level:` prefix).
- No PubMed heading invented.

## 0.16.177 — 2026-09-24

- Hundred-and-sixty-first live SearchAdapter: OpenAlex works-by-concepts.id extras (`tools.oaconcid`) grouping works via `group_by=concepts.id` with work counts, optional cites, and concepts.id-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `concid-oa` / `works-concid-oa`; `multi` includes oaconcid. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and concepts-list shape. Concept IDs are normalized to the `C…` suffix (strip URL tail / `concept:` prefix).
- No PubMed heading invented.

## 0.16.176 — 2026-09-24

- Hundred-and-sixtieth live SearchAdapter: OpenAlex works-by-keywords.id extras (`tools.oakwid`) grouping works via `group_by=keywords.id` with work counts, optional cites, and keywords.id-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `kwid-oa` / `works-kwid-oa`; `multi` includes oakwid. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and keywords-list shape. Keyword IDs keep the display string (strip URL tail / `keyword:` prefix).
- No PubMed heading invented.

## 0.16.175 — 2026-09-24

- Hundred-and-fifty-ninth live SearchAdapter: OpenAlex works-by-topics.keywords extras (`tools.oakw`) grouping works via `group_by=topics.keywords` with work counts, optional cites, and topics.keywords-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `keywords-oa` / `works-keywords-oa`; `multi` includes oakw. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and keywords-list shape. Keyword keys keep the display string (strip URL tail / `keyword:` prefix).
- No PubMed heading invented.

## 0.16.174 — 2026-09-24

- Hundred-and-fifty-eighth live SearchAdapter: OpenAlex works-by-primary_topic.id extras (`tools.oaprtopic`) grouping works via `group_by=primary_topic.id` with work counts, optional cites, and primary_topic.id-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `prtopic-oa` / `works-prtopic-oa`; `multi` includes oaprtopic. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and primary_topics-list shape. Topic IDs are normalized to the `T…` suffix (strip URL tail / `topic:` prefix).
- No PubMed heading invented.

## 0.16.173 — 2026-09-24

- Hundred-and-fifty-seventh live SearchAdapter: OpenAlex works-by-topics.domain.id extras (`tools.oatdomain`) grouping works via `group_by=topics.domain.id` with work counts, optional cites, and topics.domain.id-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `domain-oa` / `works-domain-oa`; `multi` includes oatdomain. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and domains-list shape. Domain IDs are normalized to the numeric suffix (strip URL tail / `domain:` prefix).
- No PubMed heading invented.

## 0.16.172 — 2026-09-24

- Hundred-and-fifty-sixth live SearchAdapter: OpenAlex works-by-topics.field.id extras (`tools.oatfield`) grouping works via `group_by=topics.field.id` with work counts, optional cites, and topics.field.id-filtered OpenAlex URLs. Optional `OPENALEX_MAILTO`.
- Aliases `field-oa` / `works-field-oa`; `multi` includes oatfield. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, group_by mapping (most works first), limit, and fields-list shape. Field IDs are normalized to the numeric suffix (strip URL tail / `field:` prefix).
- No PubMed heading invented.

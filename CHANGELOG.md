# Changelog

## 0.16.42 — 2026-09-18

- Twenty-sixth live SearchAdapter: OpenAlex funder extras (`tools.oafunder`) with country, alt-names, works, cites, grants, and description. Optional `OPENALEX_MAILTO`.
- Aliases `funders-oa` / `cites-funder-oa`; `multi` includes oafunder. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, payload mapping, limit, and funders-list shape.
- No PubMed heading invented.

## 0.16.41 — 2026-09-18

- Twenty-fifth live SearchAdapter: Crossref funder extras (`tools.crfunder`) with location, alt-names, work counts, and descendant work counts. Optional `CROSSREF_MAILTO`.
- Aliases `funders-cr` / `cites-funder`; `multi` includes crfunder. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, payload mapping, limit, and funders-list shape.
- No PubMed heading invented.

## 0.16.40 — 2026-09-18

- Twenty-fourth live SearchAdapter: DataCite extras (`tools.dcextra`) with publisher, subjects, rights, citation counts, language, and container. No key.
- Aliases `dc-extra` / `cites-dc`; `multi` includes dcextra. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, payload mapping, limit, and dois-list shape.
- No PubMed heading invented.

## 0.16.39 — 2026-09-18

- Twenty-third live SearchAdapter: ORCID extras (`tools.orcidextra`) with expanded-search names, institutions, other names, and ORCID iD. No key.
- Aliases `orcid-extra` / `ids-orcid`; `multi` includes orcidextra. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, payload mapping, limit, and result-list shape.
- No PubMed heading invented.

## 0.16.38 — 2026-09-18

- Twenty-second live SearchAdapter: Europe PMC extras (`tools.epmcextra`) with citation counts, OA flag, pub type, keywords, language, and abstract. Uses `resultType=core`. No key.
- Aliases `epmc-extra` / `cites-epmc`; `multi` includes epmcextra. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, payload mapping, limit, and articles-list shape.
- No PubMed heading invented.

## 0.16.37 — 2026-09-18

- Twenty-first live SearchAdapter: OpenAIRE extras (`tools.oairextra`) with access right, subjects, citation counts, publisher, language, and abstract. No key.
- Aliases `oaire-extra` / `cites-oaire`; `multi` includes oairextra. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, payload mapping, limit, and researchProducts-list shape.
- No PubMed heading invented.

## 0.16.36 — 2026-09-18

- Twentieth live SearchAdapter: OpenAlex extras (`tools.oaextra`) with citation counts, OA status, type, concepts, language, and abstract. Optional `OPENALEX_MAILTO`.
- Aliases `oa-extra` / `cites-oa`; `multi` includes oaextra. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, payload mapping, limit, and works-list shape.
- No PubMed heading invented.

## 0.16.35 — 2026-09-17

- Nineteenth live SearchAdapter: Crossref extras (`tools.xrefextra`) with citation counts, abstract, license, type, and subjects. Optional `CROSSREF_MAILTO`.
- Aliases `cr-extra` / `cites-xr`; `multi` includes xrefextra. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, payload mapping, limit, and works-list shape.
- No PubMed heading invented.

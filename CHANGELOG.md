# Changelog

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

## 0.16.34 — 2026-09-17

- Eighteenth live SearchAdapter: Unpaywall v2 title search + DOI lookup (`tools.unpaywall`) with email via `UNPAYWALL_EMAIL` (default noreply).
- Aliases `upw` / `oa-status`; `multi` includes Unpaywall. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, payload mapping, limit, and DOI-object shape.
- No PubMed heading invented.

## 0.16.33 — 2026-09-17

- Seventeenth live SearchAdapter: Semantic Scholar Graph extras (`tools.s2graph`) with tldr, citation counts, and publicationDate. No key.
- Aliases `graph-s2` / `s2-extra`; `multi` includes s2graph. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, payload mapping, limit, and papers-list shape.
- No PubMed heading invented.

## 0.16.32 — 2026-09-17

- Sixteenth live SearchAdapter: CORE v3 works search API (`tools.core`) with optional `CORE_API_KEY`.
- Aliases `coreac` / `works-core`; `multi` includes CORE. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, payload mapping, limit, and data-list shape.
- No PubMed heading invented.

## 0.16.31 — 2026-09-17

- Fifteenth live SearchAdapter: OpenAIRE Graph researchProducts API (`tools.openaire`) with no key.
- Aliases `oaire` / `graph`; `multi` includes OpenAIRE. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, payload mapping, limit, and researchProducts-list shape.
- No PubMed heading invented.

## 0.16.30 — 2026-09-17

- Fourteenth live SearchAdapter: Wikidata wbsearchentities API (`tools.wikidata`) with no key.
- Aliases `wd` / `entities`; `multi` includes Wikidata. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, payload mapping, limit, and entities-map shape.
- No PubMed heading invented.

## 0.16.29 — 2026-09-17

- Thirteenth live SearchAdapter: DOAJ articles API (`tools.doaj`) with no key.
- Aliases `oa-journals` / `journals`; `multi` includes DOAJ. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, payload mapping, limit, and articles-list shape.
- No PubMed heading invented.

## 0.16.28 — 2026-09-17

- Twelfth live SearchAdapter: DataCite DOI REST API (`tools.datacite`) with no key.
- Aliases `dc` / `dois`; `multi` includes DataCite. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, payload mapping, limit, and dois-list shape.
- No PubMed heading invented.

## 0.16.27 — 2026-09-17

- Eleventh live SearchAdapter: Zenodo records API (`tools.zenodo`) with no key.
- Aliases `zen` / `records`; `multi` includes Zenodo. Public imports stay on `tools.research`.
- Tests cover empty query, aliases, payload mapping, limit, and records-list shape.
- No PubMed heading invented.

## 0.16.26 — 2026-09-17

- Split `src/tools/kb.py` (~12k) into `kb_models`, `kb_collect`, and `kb_index` behind a slim `tools.kb` facade.
- Public imports stay on `tools.kb` (`Document`, `IndexHit`, collect/search/write helpers). Added facade re-export test.
- No PubMed heading invented.

## 0.16.25 — 2026-09-17

- Split `src/tools/research.py` (~13k) into `research_models`, `research_wiki`, and `research_dispatch` behind a slim `tools.research` facade.
- Public imports stay on `tools.research` (`Hit`, adapters, `get_adapter`, parse helpers, `search` / `record_hits`). Added facade re-export test.
- No PubMed heading invented.

## 0.16.24 — 2026-09-17

- Split `src/tools/review.py` (~13.5k) into `review_const`, `review_files`, `review_window`, `review_sketch`, and `review_digest` behind a slim `tools.review` facade.
- Public imports stay on `tools.review`. Added facade re-export test.
- No PubMed heading invented.

## 0.16.23 — 2026-09-17

- Split `src/interfaces/cli.py` (~20k, at the GitHub write limit) into `cli_const`, `cli_parser`, and a slim `cli` facade.
- Public imports stay on `interfaces.cli` (`BACKEND_HELP`, `build_parser`, `main`).
- Added facade re-export test. No PubMed heading invented.

## 0.16.22 — 2026-09-17

- Agent cycle writes today's daily review sketch (`write_cycle_daily` → `memory/reviews/daily-YYYY-MM-DD.md`) before weekly and digest so coverage lists it.
- Journal row is tagged `review`, `daily`, and `cycle`. Dry-run writes neither daily, weekly, nor digest.
- Tests cover helper tags, same-day window, cycle write-back, and dry-run skip.
- No PubMed heading invented.

## 0.16.21 — 2026-09-17

- Agent cycle writes today's weekly review sketch (`write_cycle_weekly` → `memory/reviews/weekly-YYYY-MM-DD.md`) before the digest so coverage lists it.
- Journal row is tagged `review`, `weekly`, and `cycle`. Dry-run writes neither weekly nor digest.
- Tests cover helper tags, seven-day window, cycle write-back, and dry-run skip.
- No PubMed heading invented.

## 0.16.20 — 2026-09-17

- Split `src/tools/tasks.py` (~17k) into `task_const`, `task_model`, `task_store`, and `task_ops` behind the `tools.tasks` facade.
- Public imports stay on `tools.tasks`; added a facade re-export test.
- No PubMed heading invented.

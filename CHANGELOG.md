# Changelog

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

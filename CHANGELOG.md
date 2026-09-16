# Changelog

## 0.16.0 — 2026-09-16

- Daily / weekly review sketch from journal rows + the task store (`tools.review`).
- Writes `memory/reviews/{daily|weekly}-YYYY-MM-DD.md` and a `kind=review` journal row.
- Weekly window is the seven days ending on `--day`; daily is that UTC day only.
- CLI: `eternalforge review [--day] [--period daily|weekly] [--max N] [--tag T]`.

## 0.15.0 — 2026-09-16

- Tenth live SearchAdapter: OpenAlex works API (`OpenAlexAdapter`, `parse_openalex_payload`).
- CLI `--backend openalex` (aliases: oa, works-oa).
- `MultiAdapter` now includes OpenAlex as a tenth live source.
- Payload tests do not hit the network.

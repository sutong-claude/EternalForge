# Changelog

## 0.16.10 — 2026-09-16

- Knowledge base indexes `memory/reviews/digest-*.md` as `kind=digest` / `source=digest` (daily/weekly sketches stay `review`).
- Surface digest count in `eternalforge status` as `digests=N`; `--digest` lists digest filenames.
- Persist `Digests=N` in STATE metrics on cycle via `count_digests`.
- Cycle CHANGELOG extras include `digests=N`.
- Tests cover KB classification, digest listing, status/CLI flag, and cycle write-back.

## 0.16.9 — 2026-09-16

- CLI tests for `task list --tag --status --priority --since --until`.
- Parser coverage: repeatable `--tag`, created-window `--since`/`--until`, status and priority filters.
- Integration coverage: tag match strips `#` and is case-insensitive; any-of multi-tag; inclusive created window.

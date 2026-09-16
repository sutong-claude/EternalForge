# Changelog

## 0.16.7 — 2026-09-16

- Reviews digest: `write_digest` / `render_digest` / `list_review_files` / `classify_review_name`.
- Writes `memory/reviews/digest-YYYY-MM-DD.md` and a `kind=review` journal row tagged `digest`.
- CLI: `eternalforge review --digest [--day YYYY-MM-DD]`.
- Docs: architecture coverage note for `Reviews=N`.
- Tests cover classify/list, empty digest, persist+journal, and CLI flag.

## 0.16.6 — 2026-09-16

- CLI tests for `task list --exact-id --updated-since --sort created`.
- Extracted `interfaces.cli.build_parser` for argparse coverage.

## 0.16.5 — 2026-09-16

- Surface review sketch count in `eternalforge status` as `reviews=N`.
- Persist `Reviews=N` in STATE metrics on cycle via `count_reviews` (`memory/reviews/*.md`).
- Cycle CHANGELOG extras now include `reviews=N` next to reports and tasks.
- Tests cover missing dir, markdown-only count, status wiring, and cycle write-back.

# Changelog

## 0.16.2 — 2026-09-16

- Task list filter by exact id: `Task.matches_id(..., exact=True)`; `list_tasks(..., exact_id=)`.
- Task list filter by updated window: `Task.matches_updated` / `updated_day` / `normalize_updated_day`; `list_tasks(..., updated_since=, updated_until=)` inclusive YYYY-MM-DD on the `updated` stamp.
- Tasks with an empty/invalid `updated` field are excluded when an updated window is set.
- CLI: `task list [--exact-id] [--updated-since YYYY-MM-DD] [--updated-until YYYY-MM-DD]`.

## 0.16.1 — 2026-09-16

- Restore CHANGELOG headings 0.14.0 through 0.1.0 from commit 1d508cd without dropping 0.16.0 / 0.15.0.

## 0.16.0 — 2026-09-16

- Daily / weekly review sketch from journal rows + the task store (`tools.review`).
- Writes `memory/reviews/{daily|weekly}-YYYY-MM-DD.md` and a `kind=review` journal row.
- Weekly window is the seven days ending on `--day`; daily is that UTC day only.
- CLI: `eternalforge review [--day] [--period daily|weekly] [--max N] [--tag T]`.

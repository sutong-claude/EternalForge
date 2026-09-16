# Changelog

## 0.12.3 — 2026-09-16

- Task list filter by id prefix: `Task.matches_id` / `normalize_id_prefix`; `list_tasks(..., task_id=)`.
- Task list filter by created window: `Task.matches_created` / `created_day` / `normalize_created_day`; `list_tasks(..., since=, until=)` inclusive YYYY-MM-DD on the `created` stamp.
- Tasks with an empty/invalid `created` field are excluded when a created window is set.
- CLI: `task list [--id PREFIX] [--since YYYY-MM-DD] [--until YYYY-MM-DD]`.


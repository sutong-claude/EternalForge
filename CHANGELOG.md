# Changelog

## 0.9.2 — 2026-09-15

- Persist journal `tags` on `MemoryEntry` writes (`normalize_tags`, JSONL field).
- Capture / research / report / cycle rows store kind plus optional extra tags.
- CLI: `research|capture|report --tag T` (repeatable).
- `Journal.format_recent` prints `#tags`; legacy rows without the field load as `[]`.

## 0.9.1 — 2026-09-15

- Persist compiled report count in STATE metrics on cycle (`Reports=N`).
- `bump_metrics` recounts `memory/reports/*.md` via `count_reports` when a workspace root is given.
- Tests cover missing reports dir, markdown-only count, and cycle write-back.

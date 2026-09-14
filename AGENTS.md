# EternalForge Agent Manual

You are an hourly autonomous agent working on this repository.

## Every run

1. Read `STATE.md` in full.
2. Skim `ROADMAP.md` if the phase is unclear.
3. Take **one** item from Immediate Priorities.
4. Implement it (code + tests + docs as needed).
5. Update `STATE.md` (timestamp, actions, priorities, metrics, notes).
6. Append a line to `memory/journal.jsonl` if you touched the journal helper.
7. Commit to `main` with a precise message.
8. Email hinsbesjan115@gmail.com only for significant progress. Subject prefix: `[EternalForge]`.

## Constraints

- Do not leave the tree broken.
- Prefer one complete improvement over many unfinished ones.
- Python 3.11+, no extra runtime dependencies unless truly required.
- Tests live in `tests/` and must keep passing.

# Architecture

## Principles
1. Stateful continuity via STATE.md
2. One high-leverage step per hour
3. Self-documenting tree
4. Observable commits and optional email
5. Modular tools

## Components

- `src/core/state.py` — living context
- `src/core/memory.py` — JSONL journal
- `src/core/planner.py` — single-task selection
- `src/core/agent.py` — plan-act-reflect (cycle writes today's reviews digest)
- `src/core/changelog.py` — CHANGELOG.md version sections
- `src/core/metrics.py` — Files/Tests recount and Cycles bump
- `src/interfaces/cli.py` — local operator surface
- `src/tools/research.py` — SearchAdapter + Wikipedia/fixture backends + journaled hits
- `src/tools/capture.py` — daily topic research → memory/YYYY-MM-DD.md
- `src/tools/kb.py` — inverted index over memory markdown + journal; digest-*.md is kind/source=digest
- `src/tools/review.py` — daily/weekly sketches + reviews digest (`Reviews=N`, `Digests=N`, `write_cycle_digest`)
- `src/tools/inbox.py` — Gmail/Drive listing sketch + capture-to-journal (`kind=inbox`)
- `src/tools/files.py` — workspace file helpers
- GitHub — source of truth
- Gmail — significant-progress signal

## Documentation coverage
- Review sketches live under `memory/reviews/*.md`; `count_reviews` is the source of `Reviews=N`.
- Digest files (`digest-*.md`) are counted separately (`count_digests` → `Digests=N` / status `digests=N`).
- `eternalforge review --digest` writes `memory/reviews/digest-YYYY-MM-DD.md` as a coverage note.
- A non-dry `Agent` cycle also writes that digest via `write_cycle_digest` (journal tags include `cycle`).
- `eternalforge status --digest` lists those digest filenames after the status lines.
- The knowledge base indexes digest files as `kind=digest` / `source=digest` (daily/weekly stay `review`).
- `eternalforge inbox list|capture` is offline-first (`FixtureInboxAdapter`); live Google OAuth is not wired yet.

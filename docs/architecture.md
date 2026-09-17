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
- `src/core/agent.py` — plan-act-reflect (cycle writes daily, weekly, then digest)
- `src/core/changelog.py` — CHANGELOG.md version sections
- `src/core/metrics.py` — Files/Tests recount and Cycles bump
- `src/interfaces/cli.py` — local operator surface (parser in `cli_parser`, constants in `cli_const`)
- `src/tools/research.py` — SearchAdapter + Wikipedia/fixture backends + journaled hits
- `src/tools/capture.py` — daily topic research → memory/YYYY-MM-DD.md
- `src/tools/kb.py` — inverted index over memory markdown + journal; digest-*.md is kind/source=digest; inbox journal rows are source=inbox
- `src/tools/review.py` — facade over `review_const` / `review_files` / `review_window` / `review_sketch` / `review_digest` (daily/weekly sketches + digest; `Reviews=N`, `Digests=N`, cycle writes)
- `src/tools/inbox.py` — Gmail/Drive listing + capture-to-journal (`kind=inbox`) + token probe + read-only `HttpGoogleClient` + refresh_token grant
- `src/tools/files.py` — workspace file helpers
- GitHub — source of truth
- Gmail — significant-progress signal

## Documentation coverage
- Review sketches live under `memory/reviews/*.md`; `count_reviews` is the source of `Reviews=N`.
- Digest files (`digest-*.md`) are counted separately (`count_digests` → `Digests=N` / status `digests=N`).
- `eternalforge review --digest` writes `memory/reviews/digest-YYYY-MM-DD.md` as a coverage note.
- A non-dry `Agent` cycle writes daily, then weekly, then digest (`write_cycle_daily` / `write_cycle_weekly` / `write_cycle_digest`; journal tags include `cycle`).
- `eternalforge status --digest` lists those digest filenames after the status lines.
- The knowledge base indexes digest files as `kind=digest` / `source=digest` (daily/weekly stay `review`).
- Journal rows with `kind=inbox` are indexed as `source=inbox` and tagged `inbox`.
- `count_inbox_entries` is the source of `Inbox=N` / status `inbox=N` (journal `kind=inbox` rows).
- `eternalforge inbox list|capture` is offline-first (`FixtureInboxAdapter`); `--live` uses `LiveInboxAdapter`.
- `eternalforge inbox status` reports token present/absent and `listing=no-token|google-api|expired` (no secrets in-repo).
- When a token file exists, `LiveInboxAdapter` calls a read-only Google API client (injectable in tests; default HTTP client).
- Expired access tokens are refreshed with the OAuth refresh_token grant when `refresh_token` and `client_id` are available (token file or env).

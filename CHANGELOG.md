# Changelog

## 0.16.26 — 2026-09-17

- Split `src/tools/kb.py` (~12k) into `kb_models`, `kb_collect`, and `kb_index` behind a slim `tools.kb` facade.
- Public imports stay on `tools.kb` (`Document`, `IndexHit`, collect/search/write helpers). Added facade re-export test.
- No PubMed heading invented.

## 0.16.25 — 2026-09-17

- Split `src/tools/research.py` (~13k) into `research_models`, `research_wiki`, and `research_dispatch` behind a slim `tools.research` facade.
- Public imports stay on `tools.research` (`Hit`, adapters, `get_adapter`, parse helpers, `search` / `record_hits`). Added facade re-export test.
- No PubMed heading invented.

## 0.16.24 — 2026-09-17

- Split `src/tools/review.py` (~13.5k) into `review_const`, `review_files`, `review_window`, `review_sketch`, and `review_digest` behind a slim `tools.review` facade.
- Public imports stay on `tools.review`. Added facade re-export test.
- No PubMed heading invented.

## 0.16.23 — 2026-09-17

- Split `src/interfaces/cli.py` (~20k, at the GitHub write limit) into `cli_const`, `cli_parser`, and a slim `cli` facade.
- Public imports stay on `interfaces.cli` (`BACKEND_HELP`, `build_parser`, `main`).
- Added facade re-export test. No PubMed heading invented.

## 0.16.22 — 2026-09-17

- Agent cycle writes today's daily review sketch (`write_cycle_daily` → `memory/reviews/daily-YYYY-MM-DD.md`) before weekly and digest so coverage lists it.
- Journal row is tagged `review`, `daily`, and `cycle`. Dry-run writes neither daily, weekly, nor digest.
- Tests cover helper tags, same-day window, cycle write-back, and dry-run skip.
- No PubMed heading invented.

## 0.16.21 — 2026-09-17

- Agent cycle writes today's weekly review sketch (`write_cycle_weekly` → `memory/reviews/weekly-YYYY-MM-DD.md`) before the digest so coverage lists it.
- Journal row is tagged `review`, `weekly`, and `cycle`. Dry-run writes neither weekly nor digest.
- Tests cover helper tags, seven-day window, cycle write-back, and dry-run skip.
- No PubMed heading invented.

## 0.16.20 — 2026-09-17

- Split `src/tools/tasks.py` (~17k) into `task_const`, `task_model`, `task_store`, and `task_ops` behind the `tools.tasks` facade.
- Public imports stay on `tools.tasks`; added a facade re-export test.
- No PubMed heading invented.

## 0.16.19 — 2026-09-17

- Restore truncated inbox implementation from commit `07449496` by splitting it into importable modules (`inbox_const`, `inbox_item`, `inbox_token_io`, `inbox_token_refresh`, `inbox_http`, `inbox_live`) behind `tools.inbox`.
- Env-only Google client credentials: env wins; persist pops `client_id`/`client_secret` when env is set.
- No PubMed heading invented.

## 0.16.18 — 2026-09-17

- Env-only Google client credentials: `ETERNALFORGE_GOOGLE_CLIENT_ID` / `_SECRET` override file values.
- Refresh persist drops `client_id` / `client_secret` from the token file when those env vars are set.
- `inbox status` treats env client_id + refresh_token as refreshable (`google-api`).
- Tests cover env override, stripped persist, and expired-token status with env-only client_id.
- No PubMed heading invented.

## 0.16.17 — 2026-09-17

- Refresh expired Google access tokens with the OAuth `refresh_token` grant before live listing.
- Client id/secret come from the token file or `ETERNALFORGE_GOOGLE_CLIENT_ID` / `ETERNALFORGE_GOOGLE_CLIENT_SECRET`.
- New access token is written back to the same token file; values are never logged.
- `inbox status` listing is `no-token` | `google-api` | `expired`.
- Tests cover expiry parse, dummy-opener refresh, resolve-on-expiry, and expired status.
- No PubMed heading invented.

## 0.16.16 — 2026-09-17

- Wire a read-only Google API client behind `LiveInboxAdapter` (`HttpGoogleClient` + injectable `GoogleApiClient`).
- Token JSON is parsed for `access_token` / `token` only; values are never logged.
- Live listing calls Gmail metadata + Drive file list when a token file exists; network errors yield an empty list.
- `inbox status` listing is `no-token` or `google-api` (replaces stub-empty).
- Tests cover injected client, HTTP mapping with a dummy opener, and token parse.
- No PubMed heading invented.

## 0.16.15 — 2026-09-17

- Live inbox creds probe: discover a local Google token path from `ETERNALFORGE_GOOGLE_TOKEN_PATH`, `ETERNALFORGE_CONFIG_DIR`, `<root>/.secrets/google-token.json`, or `~/.config/eternalforge/google-token.json`.
- `LiveInboxAdapter.creds_status` reports token present/absent without printing file contents; listing stays stub-empty (no Google API calls).
- CLI: `eternalforge inbox status` and `inbox list|capture --live`.
- `.gitignore` ignores `.secrets/` and `google-token.json`.
- Tests cover missing token, env path, workspace secrets file, status CLI, and empty live list.
- No PubMed heading invented.

## 0.16.14 — 2026-09-16

- Surface inbox capture count as `inbox=N` on `eternalforge status`.
- Persist `Inbox=N` in STATE metrics on cycle via `count_inbox_entries` (journal `kind=inbox`).
- Cycle CHANGELOG extras include `inbox=N`.
- Tests cover zero journal, mixed kinds, status wiring, and cycle write-back.
- No PubMed heading invented.

## 0.16.13 — 2026-09-16

- Knowledge base indexes `kind=inbox` journal rows as `source=inbox` (other journal kinds stay `source=journal`).
- Inbox documents always carry an `inbox` tag so `kb QUERY --kind inbox` / `--source inbox` / `--tag inbox` work.
- Tests cover collect + kind/source/tag filters against mixed inbox and research rows.
- No PubMed heading invented.

## 0.16.12 — 2026-09-16

- Gmail / Drive listing sketch (`tools.inbox`): `InboxItem`, fixture + live-stub adapters.
- `list_inbox` / `capture_inbox` write `kind=inbox` journal rows tagged `inbox`, `gmail`, `drive`.
- CLI: `eternalforge inbox list|capture [--source gmail|drive] [--query Q] [--offline]`.
- Live adapter returns empty until OAuth is wired. Tests stay offline.
- No PubMed heading invented.

## 0.16.11 — 2026-09-16

- Agent cycle writes today's reviews digest (`write_cycle_digest` → `memory/reviews/digest-YYYY-MM-DD.md`).
- Journal row is tagged `review`, `digest`, and `cycle`. Dry-run does not write a digest.
- Cycle metrics / CHANGELOG extras include the new digest in `Reviews=N` and `Digests=N`.
- Tests cover helper tags, cycle write-back, and dry-run skip.

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

## 0.16.8 — 2026-09-16

- CLI tests for `task list --due-soon --overdue --query`.
- Parser coverage: bare `--due-soon` defaults to 7 days; `--due-soon N` is passed through.
- Integration coverage: overdue vs due-soon vs text query against a small fixture store.

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

## 0.16.4 — 2026-09-16

- Wire CLI `task list --exact-id` / `--updated-since` / `--updated-until` to `list_tasks`.
- `--sort` accepts `created` and `updated` (aliases: age, recent/newest/new) in addition to due and priority.
- Tests cover exact-id vs prefix, updated window inclusive bounds, empty updated stamp, and created/updated sort order.

## 0.16.3 — 2026-09-16

- Knowledge base indexes `memory/reviews/*.md` as `kind=review` / `source=review`.
- Document ids use the repo-relative path (`md:memory/reviews/…`) so daily notes, reports, and reviews do not collide.
- `eternalforge kb QUERY --kind review` filters daily/weekly review sketches.
- Tests cover review collection, kind/source/tag filters, and a missing reviews directory.

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

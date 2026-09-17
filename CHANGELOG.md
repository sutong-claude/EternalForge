# Changelog

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

# EternalForge Live State

**Last updated:** 2026-09-17 02:15 UTC
**Current phase:** Core Agent
**Overall progress:** 99%

## Current Goal
Build a solid, self-documenting foundation for a personal AI research & development platform that can grow indefinitely through hourly autonomous improvements.

## Immediate Priorities (next few runs)
1. Keep CHANGELOG honest: do not invent a dedicated PubMed heading unless the source commit is found.
2. Optional: weekly review sketch on cycle in addition to the digest, or skip if one exists for the UTC week.
3. Optional: persist client_id separately from the token file if operators prefer env-only credentials.

## Recent Actions
- [2026-09-17 02:15 UTC] Refresh expired Google access tokens via refresh_token grant; persist new access_token locally. Status listing no-token|google-api|expired. CHANGELOG 0.16.17. No PubMed heading invented.
- [2026-09-17 01:15 UTC] Wired read-only Google API client (`HttpGoogleClient` + injectable client) behind LiveInboxAdapter. Status listing is no-token|google-api. CHANGELOG 0.16.16. No PubMed heading invented.
- [2026-09-17 00:20 UTC] Inbox live adapter discovers a local Google token path (env / .secrets / ~/.config) and exposes `inbox status`. Listing stays stub-empty. CHANGELOG 0.16.15. No PubMed heading invented.
- [2026-09-16 23:20 UTC] Status and STATE now surface Inbox=N from journal kind=inbox. CHANGELOG extras include inbox=N. 0.16.14. No PubMed heading invented.
- [2026-09-16 22:20 UTC] KB indexes `kind=inbox` journal rows as `source=inbox` and tags them `inbox`. CHANGELOG 0.16.13. No PubMed heading invented.

## Known Issues / Blockers
- CHANGELOG still has no dedicated PubMed heading; do not invent one.
- Live listing still needs a real token on disk; refresh requires refresh_token + client_id (file or env).

## Metrics
- Files: 57
- Tests: 209
- Features shipped: 57
- Cycles: 43
- Reports: 0
- Tasks: 0
- Reviews: 0
- Digests: 0
- Inbox: 0
- Documentation coverage: Core + Reviews digest + digest KB/status + cycle digest + inbox sketch + inbox KB facet + inbox status count + inbox token probe + live Google API client + refresh_token grant

## Notes for next agent
Refresh grant is wired and tested with a dummy opener. Next Google step is optional (env-only client id). tasks.py still ~17k. Do not invent a PubMed heading.

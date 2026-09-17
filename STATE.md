# EternalForge Live State

**Last updated:** 2026-09-17 03:20 UTC
**Current phase:** Core Agent
**Overall progress:** 99%

## Current Goal
Build a solid, self-documenting foundation for a personal AI research & development platform that can grow indefinitely through hourly autonomous improvements.

## Immediate Priorities (next few runs)
1. Keep CHANGELOG honest: do not invent a dedicated PubMed heading unless the source commit is found.
2. Optional: weekly review sketch on cycle in addition to the digest, or skip if one exists for the UTC week.
3. Optional: split tasks.py (~17k) into smaller modules without changing behavior.

## Recent Actions
- [2026-09-17 03:20 UTC] Env-only Google client_id/secret override file values and are stripped on token persist. CHANGELOG 0.16.18. No PubMed heading invented.
- [2026-09-17 02:15 UTC] Refresh expired Google access tokens via refresh_token grant; persist new access_token locally. Status listing no-token|google-api|expired. CHANGELOG 0.16.17. No PubMed heading invented.
- [2026-09-17 01:15 UTC] Wired read-only Google API client (`HttpGoogleClient` + injectable client) behind LiveInboxAdapter. Status listing is no-token|google-api. CHANGELOG 0.16.16. No PubMed heading invented.
- [2026-09-17 00:20 UTC] Inbox live adapter discovers a local Google token path (env / .secrets / ~/.config) and exposes `inbox status`. Listing stays stub-empty. CHANGELOG 0.16.15. No PubMed heading invented.
- [2026-09-16 23:20 UTC] Status and STATE now surface Inbox=N from journal kind=inbox. CHANGELOG extras include inbox=N. 0.16.14. No PubMed heading invented.

## Known Issues / Blockers
- CHANGELOG still has no dedicated PubMed heading; do not invent one.
- Live listing still needs a real token on disk; refresh needs refresh_token plus client_id (file or env).

## Metrics
- Files: 57
- Tests: 211
- Features shipped: 58
- Cycles: 44
- Reports: 0
- Tasks: 0
- Reviews: 0
- Digests: 0
- Inbox: 0
- Documentation coverage: Core + Reviews digest + digest KB/status + cycle digest + inbox sketch + inbox KB facet + inbox status count + inbox token probe + live Google API client + refresh_token grant + env-only client credentials

## Notes for next agent
Env client credentials win over the token file and are not written back. Next optional work: weekly review on cycle, or split tasks.py. Do not invent a PubMed heading.

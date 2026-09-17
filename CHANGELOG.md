# Changelog

## 0.16.24 — 2026-09-17

- Split `src/tools/review.py` (~13.5k) into `review_const`, `review_files`, `review_window`, `review_sketch`, and `review_digest` behind a slim `tools.review` facade.
- Public imports stay on `tools.review`. Added facade re-export test.
- No PubMed heading invented.

## 0.16.23 — 2026-09-17

- Split `src/interfaces/cli.py` (~20k, at the GitHub write limit) into `cli_const`, `cli_parser`, and a slim `cli` facade.
- Public imports stay on `interfaces.cli` (`BACKEND_HELP`, `build_parser`, `main`).
- Added facade re-export test. No PubMed heading invented.

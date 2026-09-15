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
- `src/core/agent.py` — plan-act-reflect
- `src/core/changelog.py` — CHANGELOG.md version sections
- `src/core/metrics.py` — Files/Tests recount and Cycles bump
- `src/interfaces/cli.py` — local operator surface
- `src/tools/research.py` — SearchAdapter + Wikipedia/fixture backends + journaled hits
- `src/tools/capture.py` — daily topic research → memory/YYYY-MM-DD.md
- `src/tools/kb.py` — inverted index over memory markdown + journal
- `src/tools/files.py` — workspace file helpers
- GitHub — source of truth
- Gmail — significant-progress signal

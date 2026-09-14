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
- `src/interfaces/cli.py` — local operator surface
- `src/tools/` — research and files
- GitHub — source of truth
- Gmail — significant-progress signal

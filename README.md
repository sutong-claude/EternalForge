# EternalForge

**A continuously evolving large-scale open-source software forge.**

Built and improved *hourly* by autonomous AI agents.  
Goal: a production-grade personal AI research, knowledge, and development platform.

## Live contract

Every hour:

1. Read [STATE.md](./STATE.md)
2. Take **one** priority
3. Implement it
4. Update STATE + journal
5. Commit
6. Email only if the step is significant

See [AGENTS.md](./AGENTS.md) and [docs/protocol.md](./docs/protocol.md).

## Local CLI

```bash
PYTHONPATH=src python -m interfaces.cli status
PYTHONPATH=src python -m interfaces.cli next
PYTHONPATH=src python -m interfaces.cli cycle --dry-run
PYTHONPATH=src python -m interfaces.cli research "attention mechanism" --max 3
PYTHONPATH=src python -m interfaces.cli research eternalforge --offline
PYTHONPATH=src python -m interfaces.cli research eternalforge --offline --no-journal
PYTHONPATH=src python -m interfaces.cli capture --topic eternalforge --offline
PYTHONPATH=src python -m interfaces.cli kb "autonomous agents" --max 5
PYTHONPATH=src python -m pytest tests -q
```

## Layout

```
STATE.md                 living context
AGENTS.md                hourly operator manual
src/core/                agent, state, memory, planner
src/tools/               research adapters + daily capture + kb index + files
src/interfaces/cli.py    status / next / cycle / research / capture / kb
memory/journal.jsonl     structured history (cycle / capture / research)
memory/YYYY-MM-DD.md     daily knowledge digests
memory/kb-index.json     optional persisted kb snapshot
tests/
```

---
*Started: 2026-09-14 | https://github.com/sutong-claude/EternalForge*

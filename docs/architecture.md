# Architecture

## Design Principles
1. **Stateful continuity** – Every run reads and writes STATE.md. Context never dies.
2. **Small, high-leverage steps** – Prefer shipping one solid improvement per hour over big incomplete changes.
3. **Self-documenting** – Code, docs and STATE stay in sync.
4. **Observable** – Clear commit messages, changelogs, and progress emails.
5. **Extensible** – Tools and capabilities are modular.

## High-level Components

### 1. Agent Core (`src/core/`)
- Planner: reads STATE + ROADMAP, selects next task
- Executor: performs the work (code, research, docs)
- Reflector: evaluates result, updates STATE
- Memory: file-based persistent context

### 2. Tools (`src/tools/`)
- File system helpers
- GitHub operations (already available via connectors)
- Research (search + summarize)
- Code generation & analysis

### 3. Interfaces
- Primary: Autonomous hourly runs
- Secondary: CLI for human interaction
- Future: Simple web dashboard

### 4. Persistence
- Primary: Git repository (STATE.md, code, docs)
- Secondary: Google Drive for large artifacts / long-term knowledge
- Tertiary: Local sandbox during a run

## Execution Model
Each hourly automation:
1. Clone / pull latest (or use GitHub tools directly)
2. Read STATE.md
3. Decide next action
4. Execute
5. Commit + push
6. Update STATE.md
7. Optionally notify via email

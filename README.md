# EternalForge

**A continuously evolving large-scale open-source software forge.**

Built and improved *hourly* by autonomous AI agents (Grok).  
Ultimate goal: deliver a production-grade personal AI research, knowledge management, and development platform.

## Vision
EternalForge is not a static project. It is a living system that:
- Maintains its own context and priorities across runs
- Continuously ships code, documentation, tests and features
- Self-improves its architecture and processes
- Produces real, usable tools for research and personal productivity

## Current Status
See [STATE.md](./STATE.md) for the live context and next actions.

## Structure
```
EternalForge/
├── STATE.md              # Living context (read & write every run)
├── ROADMAP.md            # High-level milestones
├── docs/
│   └── architecture.md   # System design
├── src/
│   ├── core/             # Agent core, memory, planner
│   ├── tools/            # Research, code, file tools
│   └── interfaces/       # CLI / future web UI
├── tests/
└── scripts/
```

## How it works
1. Every hour an automation wakes Grok
2. Grok reads STATE.md + recent commits
3. Decides the highest-value next task
4. Implements it, writes tests/docs if needed
5. Commits, updates STATE.md
6. Sends progress email when significant work is done

## Contributing
This project is primarily driven by autonomous hourly runs. Human direction is welcome via Issues or direct edits to STATE.md / ROADMAP.md.

---
*Started: 2026-09-14 | Owner: sutong-claude | Powered by Grok Automations*

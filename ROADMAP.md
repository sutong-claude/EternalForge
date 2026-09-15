# EternalForge Roadmap

## Phase 0 – Bootstrap
- [x] Create repository and vision
- [x] Directory structure and architecture doc
- [x] STATE-driven continuous improvement process

## Phase 1 – Core Agent (current)
- [x] Plan-act-reflect loop
- [x] Persistent memory (STATE.md + JSONL)
- [x] CLI surface
- [x] Research tool beyond skeleton (adapter interface + Wikipedia)
- [x] Daily knowledge capture
- [x] Persist research hits into the JSONL journal
- [x] Second live SearchAdapter (DuckDuckGo Instant Answer)
- [x] Third live SearchAdapter (Open Library) + merge-hits MultiAdapter
- [x] Knowledge-base index over memory/ markdown + journal
- [x] Journal kind filter on status / recent dump
- [x] Knowledge base query filters (kind / date)
- [x] Automated report generation from journal research hits
- [x] Index research reports in the knowledge base
- [x] Tag or source facet on KB hits
- [x] Surface report count in status
- [x] Deduplicate tags when merging journal extra_tags + extracted tags
- [x] Fourth live SearchAdapter (Hacker News Algolia)
- [x] Persist Reports=N in STATE metrics on cycle
- [x] Persist journal tags on MemoryEntry writes
- [x] Fifth live SearchAdapter (arXiv)
- [x] Journal recent dump filter by persisted tag
- [x] Task-tracking skeleton
- [x] Persist Tasks=N in STATE metrics on cycle
- [x] Task due dates / priority on the tracker
- [x] Task list sort by due/priority; overdue flag
- [x] Surface Reports/Tasks in CHANGELOG cycle extras
- [x] Task list filter by tag and due-soon window

## Phase 2 – Research Capabilities
- Additional live search backends behind SearchAdapter
- Daily/weekly review sketch

## Phase 3 – Personal Productivity Platform
- Task tracking (reviews)
- Daily/weekly review
- Gmail / Drive integration

## Phase 4 – Self-Improvement & Scale
- Automated testing gates
- Architecture evolution
- Public releases

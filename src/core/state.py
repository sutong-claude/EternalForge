"""Bidirectional STATE.md parser — the forge's living context."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
import re


@dataclass
class ForgeState:
    last_updated: str
    phase: str
    progress: float
    current_goal: str
    priorities: list[str] = field(default_factory=list)
    recent_actions: list[str] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    metrics: dict[str, str] = field(default_factory=dict)
    notes: str = ""

    def next_task(self) -> str | None:
        return self.priorities[0] if self.priorities else None

    def complete_current(self, action: str) -> None:
        if self.priorities:
            self.priorities.pop(0)
        stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        self.recent_actions.insert(0, f"[{stamp}] {action}")
        self.recent_actions = self.recent_actions[:20]
        self.last_updated = stamp


_BOLD = re.compile(r"\*\*(.+?):\*\*\s*(.+)")


def parse_state(text: str) -> ForgeState:
    lines = text.replace("\r\n", "\n").split("\n")
    fields: dict[str, str] = {}
    sections: dict[str, list[str]] = {}
    current: str | None = None
    body: list[str] = []

    def flush() -> None:
        if current is not None:
            sections[current] = body.copy()

    for raw in lines:
        line = raw.rstrip()
        if line.startswith("# "):
            continue
        if line.startswith("## "):
            flush()
            current = line[3:].strip().lower()
            body = []
            continue
        m = _BOLD.match(line)
        if m and current is None:
            fields[m.group(1).strip().lower()] = m.group(2).strip()
            continue
        if current is not None:
            body.append(line)
    flush()

    def section_text(key: str) -> str:
        for name, rows in sections.items():
            if key in name:
                return "\n".join(rows).strip()
        return ""

    def bullets(key: str) -> list[str]:
        items: list[str] = []
        for name, rows in sections.items():
            if key not in name:
                continue
            for row in rows:
                s = row.strip()
                if not s or s.startswith("#"):
                    continue
                s = re.sub(r"^(\d+\.|[-*])\s+", "", s)
                if s.lower() in {"none yet.", "none yet", "none"}:
                    continue
                items.append(s)
        return items

    progress_raw = fields.get("overall progress", "0%").replace("%", "").strip()
    try:
        progress = float(progress_raw) / 100.0 if float(progress_raw) > 1 else float(progress_raw)
        if float(progress_raw) > 1:
            progress = float(progress_raw) / 100.0
        else:
            progress = float(progress_raw)
            if progress > 1:
                progress = progress / 100.0
    except ValueError:
        progress = 0.0
    try:
        raw_n = float(progress_raw)
        progress = raw_n / 100.0 if raw_n > 1 else raw_n
    except ValueError:
        progress = 0.0

    metrics: dict[str, str] = {}
    for row in bullets("metric"):
        if ":" in row:
            k, v = row.split(":", 1)
            metrics[k.strip()] = v.strip()

    return ForgeState(
        last_updated=fields.get("last updated", ""),
        phase=fields.get("current phase", "unknown"),
        progress=progress,
        current_goal=section_text("current goal"),
        priorities=bullets("priorit"),
        recent_actions=bullets("recent"),
        blockers=bullets("blocker") or bullets("issue"),
        metrics=metrics,
        notes=section_text("notes"),
    )


def dump_state(state: ForgeState) -> str:
    pct = int(round(state.progress * 100))
    pri = "\n".join(f"{i}. {p}" for i, p in enumerate(state.priorities, 1)) or "- None yet."
    acts = "\n".join(f"- {a}" for a in state.recent_actions) or "- None yet."
    blocks = "\n".join(f"- {b}" for b in state.blockers) or "- None yet."
    mets = "\n".join(f"- {k}: {v}" for k, v in state.metrics.items()) or "- Files: 0"
    return (
        "# EternalForge Live State\n\n"
        f"**Last updated:** {state.last_updated}\n"
        f"**Current phase:** {state.phase}\n"
        f"**Overall progress:** {pct}%\n\n"
        "## Current Goal\n"
        f"{state.current_goal.strip()}\n\n"
        "## Immediate Priorities (next few runs)\n"
        f"{pri}\n\n"
        "## Recent Actions\n"
        f"{acts}\n\n"
        "## Known Issues / Blockers\n"
        f"{blocks}\n\n"
        "## Metrics\n"
        f"{mets}\n\n"
        "## Notes for next agent\n"
        f"{state.notes.strip()}\n"
    )


def load_state_file(path: Path) -> ForgeState:
    return parse_state(path.read_text(encoding="utf-8"))


def save_state_file(path: Path, state: ForgeState) -> None:
    path.write_text(dump_state(state), encoding="utf-8")

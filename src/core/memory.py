"""Append-only JSONL journal. Complements STATE.md with structured history."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json
from pathlib import Path


@dataclass
class MemoryEntry:
    timestamp: str
    kind: str
    summary: str
    details: str = ""

    @classmethod
    def now(cls, kind: str, summary: str, details: str = "") -> "MemoryEntry":
        stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        return cls(timestamp=stamp, kind=kind, summary=summary, details=details)


class Journal:
    def __init__(self, path: Path):
        self.path = path

    def append(self, entry: MemoryEntry) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(asdict(entry), ensure_ascii=False) + "\n")

    def recent(self, n: int = 20) -> list[MemoryEntry]:
        if not self.path.exists():
            return []
        lines = [ln for ln in self.path.read_text(encoding="utf-8").splitlines() if ln.strip()]
        out: list[MemoryEntry] = []
        for line in lines[-n:]:
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                continue
            if not isinstance(data, dict):
                continue
            kind = str(data.get("kind", "")).strip()
            summary = str(data.get("summary", ""))
            details = str(data.get("details", ""))
            timestamp = str(data.get("timestamp", ""))
            if not kind:
                continue
            out.append(
                MemoryEntry(
                    timestamp=timestamp,
                    kind=kind,
                    summary=summary,
                    details=details,
                )
            )
        return out

    def recent_kinds(self, n: int = 8) -> list[str]:
        """Kinds of the last n journal entries, oldest-to-newest within that window."""
        return [entry.kind for entry in self.recent(n)]

    def format_recent_kinds(self, n: int = 8) -> str:
        kinds = self.recent_kinds(n)
        return ",".join(kinds) if kinds else "-"

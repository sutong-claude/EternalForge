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


def normalize_kind(kind: str | None) -> str:
    return (kind or "").strip().lower()


class Journal:
    def __init__(self, path: Path):
        self.path = path

    def append(self, entry: MemoryEntry) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(asdict(entry), ensure_ascii=False) + "\n")

    def load(self) -> list[MemoryEntry]:
        if not self.path.exists():
            return []
        out: list[MemoryEntry] = []
        for line in self.path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                continue
            if not isinstance(data, dict):
                continue
            kind = str(data.get("kind", "")).strip()
            if not kind:
                continue
            out.append(
                MemoryEntry(
                    timestamp=str(data.get("timestamp", "")),
                    kind=kind,
                    summary=str(data.get("summary", "")),
                    details=str(data.get("details", "")),
                )
            )
        return out

    def recent(self, n: int = 20, kind: str | None = None) -> list[MemoryEntry]:
        entries = self.load()
        wanted = normalize_kind(kind)
        if wanted:
            entries = [entry for entry in entries if normalize_kind(entry.kind) == wanted]
        if n <= 0:
            return []
        return entries[-n:]

    def recent_kinds(self, n: int = 8, kind: str | None = None) -> list[str]:
        """Kinds of the last n journal entries (optionally filtered)."""
        return [entry.kind for entry in self.recent(n, kind=kind)]

    def format_recent_kinds(self, n: int = 8, kind: str | None = None) -> str:
        kinds = self.recent_kinds(n, kind=kind)
        return ",".join(kinds) if kinds else "-"

    def format_recent(self, n: int = 20, kind: str | None = None) -> str:
        entries = self.recent(n, kind=kind)
        if not entries:
            label = normalize_kind(kind) or "any"
            return f"(no journal entries kind={label})"
        lines: list[str] = []
        for entry in entries:
            lines.append(f"{entry.timestamp}\t{entry.kind}\t{entry.summary}")
            if entry.details:
                lines.append(f"\t{entry.details}")
        return "\n".join(lines)

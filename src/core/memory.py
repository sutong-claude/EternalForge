"""Append-only JSONL journal. Complements STATE.md with structured history."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Iterable


def normalize_kind(kind: str | None) -> str:
    return (kind or "").strip().lower()


def normalize_tag(tag: str | None) -> str:
    raw = (tag or "").strip().lower()
    if raw.startswith("#"):
        raw = raw[1:]
    return raw.strip()


def normalize_tags(raw: object | None) -> list[str]:
    """Order-preserving unique lowercase tags from a list, string, or None."""
    seen: dict[str, None] = {}
    items: Iterable[object]
    if raw is None:
        items = ()
    elif isinstance(raw, str):
        items = [chunk for chunk in raw.replace(";", ",").split(",")]
    elif isinstance(raw, (list, tuple)):
        items = raw
    else:
        items = [raw]
    for item in items:
        token = normalize_tag(str(item) if item is not None else "")
        if token and token not in seen:
            seen[token] = None
    return list(seen)


def entry_has_tag(entry: "MemoryEntry", tag: str | None) -> bool:
    wanted = normalize_tag(tag)
    if not wanted:
        return True
    return wanted in {normalize_tag(item) for item in entry.tags}


@dataclass
class MemoryEntry:
    timestamp: str
    kind: str
    summary: str
    details: str = ""
    tags: list[str] = field(default_factory=list)

    @classmethod
    def now(
        cls,
        kind: str,
        summary: str,
        details: str = "",
        tags: Iterable[str] | None = None,
    ) -> "MemoryEntry":
        stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        return cls(
            timestamp=stamp,
            kind=kind,
            summary=summary,
            details=details,
            tags=normalize_tags(list(tags) if tags is not None else []),
        )


class Journal:
    def __init__(self, path: Path):
        self.path = path

    def append(self, entry: MemoryEntry) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = asdict(entry)
        payload["tags"] = normalize_tags(entry.tags)
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(payload, ensure_ascii=False) + "\n")

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
                    tags=normalize_tags(data.get("tags", [])),
                )
            )
        return out

    def recent(
        self,
        n: int = 20,
        kind: str | None = None,
        tag: str | None = None,
    ) -> list[MemoryEntry]:
        entries = self.load()
        wanted = normalize_kind(kind)
        if wanted:
            entries = [entry for entry in entries if normalize_kind(entry.kind) == wanted]
        if normalize_tag(tag):
            entries = [entry for entry in entries if entry_has_tag(entry, tag)]
        if n <= 0:
            return []
        return entries[-n:]

    def recent_kinds(
        self,
        n: int = 8,
        kind: str | None = None,
        tag: str | None = None,
    ) -> list[str]:
        """Kinds of the last n journal entries (optionally filtered)."""
        return [entry.kind for entry in self.recent(n, kind=kind, tag=tag)]

    def format_recent_kinds(
        self,
        n: int = 8,
        kind: str | None = None,
        tag: str | None = None,
    ) -> str:
        kinds = self.recent_kinds(n, kind=kind, tag=tag)
        return ",".join(kinds) if kinds else "-"

    def format_recent(
        self,
        n: int = 20,
        kind: str | None = None,
        tag: str | None = None,
    ) -> str:
        entries = self.recent(n, kind=kind, tag=tag)
        if not entries:
            label = normalize_kind(kind) or "any"
            tag_label = normalize_tag(tag) or "any"
            return f"(no journal entries kind={label} tag={tag_label})"
        lines: list[str] = []
        for entry in entries:
            tag_bit = f"\t#{',#'.join(entry.tags)}" if entry.tags else ""
            lines.append(f"{entry.timestamp}\t{entry.kind}\t{entry.summary}{tag_bit}")
            if entry.details:
                lines.append(f"\t{entry.details}")
        return "\n".join(lines)

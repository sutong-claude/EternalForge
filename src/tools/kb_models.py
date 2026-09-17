"""Knowledge-base models, tokenizers, and tag/date helpers."""

from __future__ import annotations

from dataclasses import dataclass, field
import re
from typing import Iterable

TOKEN_RE = re.compile(r"[a-z0-9]+")
DAY_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")
HASH_TAG_RE = re.compile(r"(?:^|[\s(,[])#([a-zA-Z][a-zA-Z0-9_-]{0,40})\b")
TAGS_LINE_RE = re.compile(r"(?im)^tags?\s*[:=]\s*(.+)$")
SKIP_NAMES = {"kb-index.json"}


@dataclass
class Document:
    doc_id: str
    source: str
    path: str
    title: str
    text: str
    kind: str = ""
    timestamp: str = ""
    tags: list[str] = field(default_factory=list)


@dataclass
class IndexHit:
    doc_id: str
    source: str
    path: str
    title: str
    score: int
    snippet: str
    kind: str = ""
    timestamp: str = ""
    tags: list[str] = field(default_factory=list)


@dataclass
class KnowledgeIndex:
    documents: list[Document] = field(default_factory=list)
    postings: dict[str, list[tuple[str, int]]] = field(default_factory=dict)

    def document_count(self) -> int:
        return len(self.documents)


def tokenize(text: str) -> list[str]:
    return TOKEN_RE.findall((text or "").lower())


def extract_day(value: str | None) -> str | None:
    if not value:
        return None
    match = DAY_RE.search(str(value))
    return match.group(1) if match else None


def parse_day(value: str | None) -> str | None:
    raw = (value or "").strip()
    if not raw:
        return None
    day = extract_day(raw)
    if day is None or not raw.startswith(day):
        raise ValueError(f"invalid date {value!r} (expected YYYY-MM-DD)")
    return day


def normalize_kind(kind: str | None) -> str:
    return (kind or "").strip().lower()


def normalize_tag(tag: str | None) -> str:
    raw = (tag or "").strip().lower()
    if raw.startswith("#"):
        raw = raw[1:]
    return raw.strip()


def merge_tags(*groups: Iterable[str] | None) -> list[str]:
    seen: dict[str, None] = {}
    for group in groups:
        if not group:
            continue
        for raw in group:
            token = normalize_tag(str(raw) if raw is not None else "")
            if token and token not in seen:
                seen[token] = None
    return list(seen)


def extract_tags(*parts: str) -> list[str]:
    seen: dict[str, None] = {}
    for part in parts:
        text = part or ""
        for match in TAGS_LINE_RE.finditer(text):
            payload = match.group(1)
            for chunk in re.split(r"[,;]+", payload):
                token = normalize_tag(chunk)
                if token and token not in seen:
                    seen[token] = None
        for match in HASH_TAG_RE.finditer(text):
            token = normalize_tag(match.group(1))
            if token and token not in seen:
                seen[token] = None
    return list(seen)


def journal_extra_tags(raw_tags: object) -> list[str]:
    if isinstance(raw_tags, str):
        return extract_tags(f"tags: {raw_tags}")
    if isinstance(raw_tags, list):
        return merge_tags(raw_tags)
    return []


def journal_source(kind: str | None) -> str:
    """Facet for a journal row. Inbox captures are source=inbox, not generic journal."""
    if normalize_kind(kind) == "inbox":
        return "inbox"
    return "journal"


def journal_kind_tags(kind: str | None) -> list[str]:
    if normalize_kind(kind) == "inbox":
        return ["inbox"]
    return []


def document_matches(
    doc: Document,
    kind: str | None = None,
    since: str | None = None,
    until: str | None = None,
    source: str | None = None,
    tag: str | None = None,
) -> bool:
    wanted = normalize_kind(kind)
    if wanted and normalize_kind(doc.kind) != wanted and normalize_kind(doc.source) != wanted:
        return False
    wanted_source = normalize_kind(source)
    if wanted_source and normalize_kind(doc.source) != wanted_source:
        return False
    wanted_tag = normalize_tag(tag)
    if wanted_tag:
        doc_tags = {normalize_tag(t) for t in doc.tags}
        if wanted_tag not in doc_tags:
            return False
    since_day = extract_day(since) if since else None
    until_day = extract_day(until) if until else None
    if since_day or until_day:
        day = extract_day(doc.timestamp)
        if day is None:
            return False
        if since_day and day < since_day:
            return False
        if until_day and day > until_day:
            return False
    return True

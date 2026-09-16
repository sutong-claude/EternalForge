"""Knowledge-base index over memory/ markdown, reports, reviews, and the JSONL journal.

Rebuilds in-memory from disk (no network). Optional snapshot at
memory/kb-index.json for inspection by later tools.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
import json
from pathlib import Path
import re
from typing import Iterable

TOKEN_RE = re.compile(r"[a-z0-9]+")
DAY_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")
HASH_TAG_RE = re.compile(r"(?:^|[\s(,\[])#([a-zA-Z][a-zA-Z0-9_-]{0,40})\b")
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


def _title_from_markdown(text: str, fallback: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            return stripped.lstrip("#").strip() or fallback
    return fallback


def _snippet(text: str, query_tokens: list[str], width: int = 160) -> str:
    raw = " ".join((text or "").split())
    if not raw:
        return ""
    lower = raw.lower()
    pos = 0
    for tok in query_tokens:
        found = lower.find(tok)
        if found >= 0:
            pos = max(0, found - 24)
            break
    chunk = raw[pos : pos + width]
    if pos > 0:
        chunk = "…" + chunk
    if pos + width < len(raw):
        chunk = chunk.rstrip() + "…"
    return chunk


def _markdown_kind_and_source(rel: str) -> tuple[str, str]:
    """Classify a memory-relative markdown path."""
    posix = rel.replace("\\", "/")
    if posix.startswith("memory/reports/") or "/reports/" in f"/{posix}":
        return "report", "report"
    if posix.startswith("memory/reviews/") or "/reviews/" in f"/{posix}":
        name = posix.rsplit("/", 1)[-1].lower()
        if name.startswith("digest-"):
            return "digest", "digest"
        return "review", "review"
    return "markdown", "markdown"


def _add_markdown_docs(docs: list[Document], root: Path, paths: list[Path]) -> None:
    for path in paths:
        if path.name in SKIP_NAMES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        rel = path.relative_to(root).as_posix()
        kind, source = _markdown_kind_and_source(rel)
        day = extract_day(path.name) or extract_day(rel)
        docs.append(
            Document(
                doc_id=f"md:{rel}",
                source=source,
                path=rel,
                title=_title_from_markdown(text, path.name),
                text=text,
                kind=kind,
                timestamp=day or "",
                tags=extract_tags(text),
            )
        )


def collect_documents(root: Path) -> list[Document]:
    memory = root / "memory"
    docs: list[Document] = []
    if not memory.exists():
        return docs
    top_level = sorted(memory.glob("*.md"))
    reports_dir = memory / "reports"
    report_files = sorted(reports_dir.glob("*.md")) if reports_dir.is_dir() else []
    reviews_dir = memory / "reviews"
    review_files = sorted(reviews_dir.glob("*.md")) if reviews_dir.is_dir() else []
    _add_markdown_docs(docs, root, top_level + report_files + review_files)
    journal = memory / "journal.jsonl"
    if journal.exists():
        try:
            lines = journal.read_text(encoding="utf-8").splitlines()
        except OSError:
            lines = []
        for idx, line in enumerate(lines):
            if not line.strip():
                continue
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                continue
            if not isinstance(data, dict):
                continue
            kind = str(data.get("kind", "")).strip()
            summary = str(data.get("summary", ""))
            details = str(data.get("details", ""))
            timestamp = str(data.get("timestamp", "")).strip()
            if not kind and not summary and not details:
                continue
            extra_tags = journal_extra_tags(data.get("tags", []))
            title = f"{kind or 'entry'}: {summary}".strip()
            body = " ".join(part for part in (kind, summary, details) if part)
            docs.append(
                Document(
                    doc_id=f"journal:{idx}",
                    source=journal_source(kind),
                    path="memory/journal.jsonl",
                    title=title[:120],
                    text=body,
                    kind=kind or "journal",
                    timestamp=timestamp,
                    tags=merge_tags(
                        extract_tags(summary, details),
                        extra_tags,
                        journal_kind_tags(kind),
                    ),
                )
            )
    return docs


def build_index(documents: list[Document] | None = None, root: Path | None = None) -> KnowledgeIndex:
    docs = list(documents) if documents is not None else collect_documents(root or Path.cwd())
    postings: dict[str, list[tuple[str, int]]] = {}
    for doc in docs:
        counts: dict[str, int] = {}
        for tok in tokenize(f"{doc.title} {doc.text}"):
            counts[tok] = counts.get(tok, 0) + 1
        for tok, tf in counts.items():
            postings.setdefault(tok, []).append((doc.doc_id, tf))
    return KnowledgeIndex(documents=docs, postings=postings)


def search_index(
    index: KnowledgeIndex,
    query: str,
    max_results: int = 8,
    kind: str | None = None,
    since: str | None = None,
    until: str | None = None,
    source: str | None = None,
    tag: str | None = None,
) -> list[IndexHit]:
    tokens = tokenize(query)
    if not tokens or not index.documents:
        return []
    allowed = {
        doc.doc_id
        for doc in index.documents
        if document_matches(
            doc, kind=kind, since=since, until=until, source=source, tag=tag
        )
    }
    if not allowed:
        return []
    by_id = {doc.doc_id: doc for doc in index.documents}
    scores: dict[str, int] = {}
    for tok in tokens:
        for doc_id, tf in index.postings.get(tok, ()):
            if doc_id not in allowed:
                continue
            scores[doc_id] = scores.get(doc_id, 0) + tf
    ranked = sorted(scores.items(), key=lambda item: (-item[1], item[0]))
    hits: list[IndexHit] = []
    for doc_id, score in ranked[: max(0, max_results)]:
        doc = by_id[doc_id]
        hits.append(
            IndexHit(
                doc_id=doc.doc_id,
                source=doc.source,
                path=doc.path,
                title=doc.title,
                score=score,
                snippet=_snippet(doc.text, tokens),
                kind=doc.kind,
                timestamp=doc.timestamp,
                tags=list(doc.tags),
            )
        )
    return hits


def search_kb(
    root: Path,
    query: str,
    max_results: int = 8,
    kind: str | None = None,
    since: str | None = None,
    until: str | None = None,
    source: str | None = None,
    tag: str | None = None,
) -> list[IndexHit]:
    return search_index(
        build_index(root=root),
        query,
        max_results=max_results,
        kind=kind,
        since=since,
        until=until,
        source=source,
        tag=tag,
    )


def format_index_hits(hits: list[IndexHit]) -> str:
    if not hits:
        return "(no matches)"
    lines: list[str] = []
    for hit in hits:
        meta = hit.kind or hit.source
        stamp = f" {hit.timestamp}" if hit.timestamp else ""
        tag_bit = f" #{',#'.join(hit.tags)}" if hit.tags else ""
        source_bit = f" src={hit.source}" if hit.source and hit.source != meta else ""
        lines.append(f"[{hit.score}] {hit.title} ({meta}{stamp}{source_bit}{tag_bit} {hit.path})")
        if hit.snippet:
            lines.append(f"    {hit.snippet}")
    return "\n".join(lines)


def write_index(index: KnowledgeIndex, root: Path) -> Path:
    memory = root / "memory"
    memory.mkdir(parents=True, exist_ok=True)
    path = memory / "kb-index.json"
    payload = {
        "document_count": index.document_count(),
        "token_count": len(index.postings),
        "documents": [asdict(doc) for doc in index.documents],
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path

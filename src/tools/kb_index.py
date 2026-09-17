"""Build, search, format, and persist the knowledge-base index."""

from __future__ import annotations

from dataclasses import asdict
import json
from pathlib import Path

from tools.kb_collect import collect_documents
from tools.kb_models import Document, IndexHit, KnowledgeIndex, document_matches, tokenize


def snippet(text: str, query_tokens: list[str], width: int = 160) -> str:
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
        chunk = "\u2026" + chunk
    if pos + width < len(raw):
        chunk = chunk.rstrip() + "\u2026"
    return chunk


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
                snippet=snippet(doc.text, tokens),
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

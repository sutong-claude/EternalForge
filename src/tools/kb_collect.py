"""Collect knowledge-base documents from memory markdown and the journal."""

from __future__ import annotations

import json
from pathlib import Path

from tools.kb_models import (
    SKIP_NAMES,
    Document,
    extract_day,
    extract_tags,
    journal_extra_tags,
    journal_kind_tags,
    journal_source,
    merge_tags,
)


def _title_from_markdown(text: str, fallback: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            return stripped.lstrip("#").strip() or fallback
    return fallback


def markdown_kind_and_source(rel: str) -> tuple[str, str]:
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


def add_markdown_docs(docs: list[Document], root: Path, paths: list[Path]) -> None:
    for path in paths:
        if path.name in SKIP_NAMES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        rel = path.relative_to(root).as_posix()
        kind, source = markdown_kind_and_source(rel)
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
    add_markdown_docs(docs, root, top_level + report_files + review_files)
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

"""Knowledge-base index over memory/ markdown, reports, reviews, and the JSONL journal.

Rebuilds in-memory from disk (no network). Optional snapshot at
memory/kb-index.json for inspection by later tools.

Implementation is split into kb_models / kb_collect / kb_index;
this module is the public facade so imports stay `tools.kb`.
"""

from __future__ import annotations

from tools.kb_collect import add_markdown_docs, collect_documents, markdown_kind_and_source
from tools.kb_index import (
    build_index,
    format_index_hits,
    search_index,
    search_kb,
    snippet,
    write_index,
)
from tools.kb_models import (
    DAY_RE,
    HASH_TAG_RE,
    SKIP_NAMES,
    TAGS_LINE_RE,
    TOKEN_RE,
    Document,
    IndexHit,
    KnowledgeIndex,
    document_matches,
    extract_day,
    extract_tags,
    journal_extra_tags,
    journal_kind_tags,
    journal_source,
    merge_tags,
    normalize_kind,
    normalize_tag,
    parse_day,
    tokenize,
)

# Historical private names used by older callers.
_add_markdown_docs = add_markdown_docs
_markdown_kind_and_source = markdown_kind_and_source
_snippet = snippet

__all__ = [
    "DAY_RE",
    "HASH_TAG_RE",
    "SKIP_NAMES",
    "TAGS_LINE_RE",
    "TOKEN_RE",
    "Document",
    "IndexHit",
    "KnowledgeIndex",
    "build_index",
    "collect_documents",
    "document_matches",
    "extract_day",
    "extract_tags",
    "format_index_hits",
    "journal_extra_tags",
    "journal_kind_tags",
    "journal_source",
    "merge_tags",
    "normalize_kind",
    "normalize_tag",
    "parse_day",
    "search_index",
    "search_kb",
    "tokenize",
    "write_index",
]

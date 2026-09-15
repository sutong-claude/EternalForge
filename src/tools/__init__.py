"""Tools for the EternalForge agent."""

from tools.capture import CaptureResult, capture
from tools.kb import IndexHit, KnowledgeIndex, build_index, search_kb
from tools.report import ReportResult, count_reports, write_report
from tools.research import Hit, SearchAdapter, get_adapter, record_hits, search, summarize

__all__ = [
    "Hit",
    "SearchAdapter",
    "search",
    "summarize",
    "record_hits",
    "get_adapter",
    "capture",
    "CaptureResult",
    "IndexHit",
    "KnowledgeIndex",
    "build_index",
    "search_kb",
    "write_report",
    "count_reports",
    "ReportResult",
]

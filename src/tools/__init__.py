"""Tools for the EternalForge agent."""

from tools.capture import CaptureResult, capture
from tools.inbox import (
    InboxCaptureResult,
    InboxItem,
    capture_inbox,
    count_inbox_entries,
    format_items,
    list_inbox,
)
from tools.kb import IndexHit, KnowledgeIndex, build_index, search_kb
from tools.report import ReportResult, count_reports, write_report
from tools.research import Hit, SearchAdapter, get_adapter, record_hits, search, summarize
from tools.review import (
    DigestResult,
    ReviewResult,
    count_digests,
    count_reviews,
    write_cycle_digest,
    write_digest,
    write_review,
)
from tools.tasks import Task, add_task, count_open_tasks, list_tasks, set_task_status, sort_tasks, update_task

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
    "write_review",
    "write_digest",
    "write_cycle_digest",
    "count_reviews",
    "count_digests",
    "ReviewResult",
    "DigestResult",
    "Task",
    "add_task",
    "list_tasks",
    "sort_tasks",
    "set_task_status",
    "update_task",
    "count_open_tasks",
    "InboxItem",
    "InboxCaptureResult",
    "list_inbox",
    "capture_inbox",
    "count_inbox_entries",
    "format_items",
]

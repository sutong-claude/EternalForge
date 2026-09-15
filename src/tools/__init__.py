"""Tools for the EternalForge agent."""

from tools.capture import CaptureResult, capture
from tools.kb import IndexHit, KnowledgeIndex, build_index, search_kb
from tools.report import ReportResult, count_reports, write_report
from tools.research import Hit, SearchAdapter, get_adapter, record_hits, search, summarize
from tools.tasks import Task, add_task, count_open_tasks, list_tasks, set_task_status, update_task

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
    "Task",
    "add_task",
    "list_tasks",
    "set_task_status",
    "update_task",
    "count_open_tasks",
]

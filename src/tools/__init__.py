"""Tools for the EternalForge agent."""

from tools.capture import CaptureResult, capture
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
]

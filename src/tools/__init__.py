"""Tools for the EternalForge agent."""

from tools.capture import CaptureResult, capture
from tools.research import Hit, SearchAdapter, record_hits, search, summarize

__all__ = [
    "Hit",
    "SearchAdapter",
    "search",
    "summarize",
    "record_hits",
    "capture",
    "CaptureResult",
]
